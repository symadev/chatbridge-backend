from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.utils.auth import get_current_user
from app.database.mongodb import get_messages_collection
from app.models.chat import ChatMessageResponse

# RAG imports
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os

router = APIRouter(prefix="/chat", tags=["Chat"])

# RAG setup
openai_client = OpenAI()
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# Qdrant client initialization
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collection_name = "learning_rag"

# Check if collection exists, if not create it
try:
    collections = qdrant_client.get_collections().collections
    collection_exists = any(col.name == collection_name for col in collections)
    
    if not collection_exists:
        print(f"Collection '{collection_name}' not found. Creating...")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=3072,  # text-embedding-3-large dimension
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{collection_name}' created successfully!")
    else:
        print(f"Collection '{collection_name}' already exists.")
    
    # Connect to vector store
    vector_db = QdrantVectorStore.from_existing_collection(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=collection_name,
        embedding=embedding_model,
    )
    print("Connected to Qdrant successfully!")
    
except Exception as e:
    print(f"Error setting up Qdrant: {e}")
    raise

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    message_id: str

@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user)
):
    """Send message and get the response"""
    
    # RAG logic
    search_results = vector_db.similarity_search(query=request.message, k=4)
    
    context = "\n\n\n".join([
        f"Page Content: {result.page_content}\nPage Number: {result.metadata.get('page_label', 'N/A')}" 
        for result in search_results
    ])
    
    SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers user queries based on the available context retrieved from a PDF file along with page contents and page number.
You should only answer the user based on the following context and no need to include the page number but if user asks you a question then try to answer in few sentences. Try to be concise. You can also talk cordially about personal problems.
If the user query is not related to the context, politely inform them: "Sorry, I can only answer questions related to the provided context."

Context:
{context}
"""
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.message},
        ]
    )
    
    bot_reply = response.choices[0].message.content
    
    # Save to database
    messages_collection = get_messages_collection()
    message_data = {
        "user_id": user_id,
        "message": request.message,
        "response": bot_reply,
        "timestamp": datetime.utcnow()
    }
    
    result = await messages_collection.insert_one(message_data)
    
    return {
        "reply": bot_reply,
        "message_id": str(result.inserted_id)
    }

@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    user_id: str = Depends(get_current_user),
    limit: int = 50
):
    """Load the chat history"""
    messages_collection = get_messages_collection()
    
    cursor = messages_collection.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(limit)
    
    messages = await cursor.to_list(length=limit)
    
    return [
        {
            "id": str(msg["_id"]),
            "message": msg["message"],
            "response": msg["response"],
            "timestamp": msg["timestamp"]
        }
        for msg in messages
    ]
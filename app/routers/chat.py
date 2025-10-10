from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.utils.auth import get_current_user
from app.database.mongodb import get_messages_collection
from app.models.chat import ChatMessageResponse

# RAG imports (from my existing code)
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os

router = APIRouter(prefix="/chat", tags=["Chat"])

# RAG setup (from my existing code)
openai_client = OpenAI()
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
vector_db = QdrantVectorStore.from_existing_collection(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    collection_name="learning_rag",
    embedding=embedding_model,
)

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
    """send mgs and get the response"""
    
    # RAG logic (from existing code)
    search_results = vector_db.similarity_search(query=request.message, k=4)
    
    context = "\n\n\n".join([
        f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}" 
        for result in search_results
    ])
    
    SYSTEM_PROMPT = f"""
  You are a helpful AI Assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page number.
    You should only answer the user based on the following context and no need to including the page number but if user ask you a question then try to answer in few sentence.Try to concise it. You can also talk cordially about personal problems.
    if the use query is not related to the context, politely inform them  sorry ,you can only answer questions related to the provided context.
    Context:
    
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
    
    # Save to database #database a mgs gulo save hocce
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
    """load the chat history"""
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
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

app = FastAPI()
openai_client = OpenAI()

# ✅ CORS setup
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Vector DB connection (একবার load করো)
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)

# Input/Output models
class MessageRequest(BaseModel):
    text: str

class MessageResponse(BaseModel):
    reply: str

# ✅ POST endpoint with RAG logic
@app.post("/chat", response_model=MessageResponse)
async def chat_endpoint(request: MessageRequest):
    user_query = request.text
    
    # Vector DB থেকে relevant chunks খুঁজে বের করো
    search_results = vector_db.similarity_search(query=user_query, k=4)
    
    # Context তৈরি করো
    context = "\n\n\n".join([
        f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" 
        for result in search_results
    ])
    
    # System prompt
    SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page number.
    You should only answer the user based on the following context and navigate the user to open the right page number to know more. You can also talk cordially about personal problems.
    
    Context:
    {context}
    """
    
    # OpenAI API call
    response = openai_client.chat.completions.create(
        model="gpt-5",  # ⚠️ "gpt-5" এখনো নেই, "gpt-4o" বা "gpt-4" use করো
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ]
    )
    
    bot_reply = response.choices[0].message.content
    
    return {"reply": bot_reply}
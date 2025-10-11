from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os

load_dotenv()

# PDF path
pdf_path = Path(__file__).parent / "13-Human.pdf"

print("Loading PDF...")
# Load PDF
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()
print(f"Loaded {len(docs)} pages")

# Split into chunks
print(" Splitting documents...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(documents=docs)
print(f"Created {len(chunks)} chunks")

# Vector Embeddings
print("Creating embeddings...")
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Upload to Qdrant Cloud
print("Uploading to Qdrant Cloud...")
try:
    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name="learning_rag",
        force_recreate=True  # 
    )
    print(" Successfully uploaded to Qdrant Cloud!")
    print(f" Collection: learning_rag")
    print(f" URL: {os.getenv('QDRANT_URL')}")
except Exception as e:
    print(f" Error uploading to Qdrant: {e}")
    raise
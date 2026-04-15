from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database.mongodb import MongoDB
from app.routers import auth, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    MongoDB.connect_db()
    yield
    MongoDB.close_db()

app = FastAPI(title="ChatBridge API", lifespan=lifespan)

# CORS
origins = [
    "https://chatbridge-lemon.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers # aiakhe amra just rouet gulo load korlam
app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "ChatBridge API is running!"}


@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"message": "Server is running"}

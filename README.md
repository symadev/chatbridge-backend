# 🤖 ChatBridge Backend – AI-Powered RAG API

<p align="center">
  <a href="https://github.com/symadev/chatbridge-backend">
    <img src="https://img.shields.io/badge/Live-API-success?style=for-the-badge&logo=fastapi" />
  </a>
  <a href="https://github.com/symadev/chatbridge">
    <img src="https://img.shields.io/badge/Frontend-Repo-blue?style=for-the-badge&logo=react" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  </a>
</p>

---

## 📘 About

**ChatBridge Backend** is a FastAPI application that uses **Retrieval-Augmented Generation (RAG)** to enable intelligent conversations with PDF documents.  
Ask questions and get **AI-powered answers** with **exact page references**.

---

## 🛠️ Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/-LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/-Qdrant-24386C?style=for-the-badge&logo=qdrant&logoColor=white" />
  <img src="https://img.shields.io/badge/-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

---

## ✨ Features

### 🔐 **Authentication**
- ✅ **JWT Authentication** – Secure token-based auth system  
- ✅ **Password Hashing** – Bcrypt encryption for user security  
- ✅ **Protected Routes** – Automatic authorization checks  

---

### 💬 **Chat Features**
- ✅ **Message History** – Persistent chat storage in MongoDB  
- ✅ **Real-time Responses** – Fast AI-powered answers  
- ✅ **Source Citations** – Referenced PDF pages for transparency  
- ✅ **User-specific Data** – Each user has their own chat history  

---

### 🤖 **RAG Pipeline**
- ✅ **PDF Indexing** – Automatic document processing  
- ✅ **Vector Search** – Semantic similarity using Qdrant  
- ✅ **Context-Aware AI** – GPT-5 with document context  
- ✅ **Page References** – Exact page numbers in responses  

---

## 🎬 Live Demo

👉 **[Try ChatBridge Backend](https://github.com/symadev/chatbridge-backend)**

---

## 🚀 Installation & Setup

Follow these steps to set up and run the ChatBridge Backend locally 👇


# 1️⃣ Clone the repository

```bash
git clone https://github.com/symadev/chatbridge-backend.git
```

# 2️⃣ Navigate to the project directory

```bash
cd chatbridge-backend
```

# 3️⃣ Create a virtual environment (Windows)

```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

# 💻 For Mac/Linux

```bash
source venv/bin/activate
```

# 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
# or

```bash
yarn install
```

# 5️⃣ Start Qdrant database

```bash
cd app/rag
```
```bash
docker-compose up -d
```

# 6️⃣ Index PDF documents (first time only)

```bash
python index.py
```

# 7️⃣ Start the development server
```bash
cd ../..
```
```bash
uvicorn app.main:app --reload
```
# or

```bash
yarn dev

```

# 8️⃣ Open your browser

```bash
http://localhost:8000/chat

```

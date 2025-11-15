# 🚀 Simple RAG Application
Qdrant • LlamaIndex • Ollama • FastAPI • Inngest • Streamlit • uv

This project is a fully open-source Retrieval-Augmented Generation (RAG) application that runs 100% locally.

## 📦 Features
- Document ingestion (PDF, TXT, MD)
- LlamaIndex chunking + embedding
- Qdrant vector storage
- Retrieval-Augmented Generation
- Local LLM via Ollama
- Background jobs using Inngest
- FastAPI backend
- Streamlit UI
- Fully offline

## 🧰 New System Setup
### Install Python
https://www.python.org/downloads/

### Install uv
pip install uv

### Install Ollama
https://ollama.com/download  
ollama pull llama3

### Install Docker (for Qdrant)
https://www.docker.com/products/docker-desktop/

### Install Dependencies
uv sync  
or  
pip install -r requirements.txt

## 🚀 Run Application (4 Terminals)
### Terminal 1: Start Qdrant
Windows:
docker run -p 6333:6333 -v "${pwd}/qdrant_storage:/qdrant/storage" qdrant/qdrant

Mac/Linux:
docker run -p 6333:6333 -v "$(pwd)/qdrant_storage:/qdrant/storage" qdrant/qdrant

### Terminal 2: Start FastAPI
uv run uvicorn main:app --reload  
or  
uvicorn main:app --reload

### Terminal 3: Start Inngest
npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery

### Terminal 4: Start Streamlit
uv run streamlit run streamlit_ui.py  
or  
streamlit run streamlit_ui.py

## 📥 Ingest Documents
curl -X POST http://127.0.0.1:8000/ingest

## 🔍 Query Example
curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d '{"query":"What is this project about?", "top_k":5}'

## 📂 Project Structure
Rag_Application/
│── main.py  
│── streamlit_ui.py  
│── inngest_workflows/  
│── qdrant_storage/  
│── data/  
│── pyproject.toml  
│── requirements.txt  
│── README.md

## 🔒 .env Example
QDRANT_URL=http://localhost:6333  
LLM_MODEL=llama3  
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2

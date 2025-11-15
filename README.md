# Rag_Application
Simple RAG app using open-source LLMs &amp; vector DBs — local embeddings, retrieval, and generation (Ollama/Inngest/Qdrant)


# Simple RAG Application (Qdrant + LlamaIndex + Ollama + Inngest)

A lightweight Retrieval-Augmented Generation (RAG) application built entirely with **open-source tools**.  
This project demonstrates how to ingest documents, store embeddings in Qdrant, retrieve relevant chunks using LlamaIndex, generate answers with Ollama-hosted LLMs, and orchestrate background tasks using Inngest.

---

## 🚀 Tech Stack

### **Core Components**
- **Ollama** – local LLM runtime for fast, offline text generation  
- **LlamaIndex** – indexing, retrieval, query engine, RAG orchestration  
- **Qdrant** – high-performance vector database for embedding storage  
- **Inngest** – background workflows for ingestion, chunking, vector updates, etc.

---

## 📌 Features

- Ingest PDFs, text, or markdown files  
- Automatic chunking + embedding generation via LlamaIndex  
- Vector storage & similarity search using **Qdrant**  
- Local LLM inference powered by **Ollama**  
- Async workflows triggered via **Inngest**  
- Clean retrieval pipeline (top-k search → context → prompt construction)  
- FastAPI-based API endpoints for chat/query  
- Source citations + provenance in responses  

---

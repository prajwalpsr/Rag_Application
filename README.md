# 🚀 Simple RAG Application  
### **Qdrant + LlamaIndex + Ollama + FastAPI + Inngest + Streamlit**

A fully open-source Retrieval-Augmented Generation (RAG) application built using:

- **Qdrant** – Vector Database  
- **LlamaIndex** – Chunking, Embeddings & RAG Engine  
- **Ollama** – Local LLM Inference (Llama3 or any open model)  
- **FastAPI** – Backend API  
- **Inngest** – Background workflows for ingestion  
- **Streamlit** – Frontend UI  
- **uv** – Fast Python environment manager and dependency installer

This project demonstrates how to build a clean, local-first RAG pipeline that requires **no paid APIs** and can run completely offline.

---

# 📦 Features

- 📄 PDF / TXT / MD document ingestion  
- 🔍 Vector search using Qdrant  
- 🤖 Local LLM inference powered by Ollama  
- ⚡ LlamaIndex RAG pipeline (chunking → embedding → retrieval → synthesis)  
- 🔁 Inngest background workflows  
- 🖥️ Streamlit UI for user interaction  
- 🔌 FastAPI backend with clean endpoints  
- 🗄️ Persistent vector storage  
- 💡 Works entirely offline  

---

# 🛠️ Tech Stack

| Component      | Purpose |
|----------------|---------|
| **Qdrant**     | Vector DB to store embeddings |
| **LlamaIndex** | Chunking, embedding, retrieval |
| **Ollama**     | Local LLM inference |
| **FastAPI**    | Backend server |
| **Inngest**    | Async workflows (ingestion jobs) |
| **Streamlit**  | User interface |
| **uv**         | Python env + dependency manager |

---

# 🔧 Installation (New System Setup)

Follow these steps on any new machine before running the app.

## **1️⃣ Install Python**
https://www.python.org/downloads/

---

## **2️⃣ Install uv**
```bash
pip install uv

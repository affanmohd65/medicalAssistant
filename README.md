# 🏥 MediBot — AI Medical Assistant

> An intelligent RAG-powered medical assistant that answers health questions based on uploaded medical documents using LangChain, Pinecone, Groq LLM, FastAPI, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.3-yellow?style=for-the-badge)
![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-purple?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [RAG Pipeline](#-rag-pipeline)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🧠 Overview

**MediBot** is a Retrieval-Augmented Generation (RAG) application that allows users to upload medical PDF documents and ask health-related questions. The system retrieves relevant context from the uploaded documents and generates accurate, document-grounded answers using a powerful LLM — without hallucinating or making up medical facts.

> ⚠️ **Disclaimer:** MediBot is for informational purposes only. It does not provide medical diagnoses or professional medical advice. Always consult a qualified healthcare professional.

---

## ✨ Features

- 📄 **Upload Medical PDFs** — Upload one or multiple medical documents
- 💬 **Conversational Q&A** — Chat interface with full conversation history
- 🔍 **RAG Pipeline** — Retrieves relevant context before answering
- 🧠 **Groq LLM** — Powered by `llama-3.3-70b-versatile` for fast, accurate responses
- 📌 **Source Citations** — Shows which document the answer came from
- ⬇️ **Download Chat History** — Export your conversation as a `.txt` file
- 🛡️ **Global Exception Handling** — Middleware catches all errors gracefully
- 📋 **Structured Logging** — All events logged to console and file

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | FastAPI + Uvicorn |
| **LLM** | Groq (`llama-3.3-70b-versatile`) |
| **Embeddings** | HuggingFace (`all-mpnet-base-v2`) |
| **Vector Database** | Pinecone |
| **RAG Framework** | LangChain |
| **PDF Loader** | PyPDFLoader |
| **Text Splitting** | RecursiveCharacterTextSplitter |
| **Logging** | Python `logging` + RotatingFileHandler |

---

## 📁 Project Structure

```
DOCTORASSISTANT/
│
├── client/                          # 🖥️ Streamlit Frontend
│   ├── components/
│   │   ├── upload.py                # PDF upload UI component
│   │   ├── chat.py                  # Chat interface component
│   │   └── history_download.py      # Download chat history
│   ├── utils/
│   │   └── api.py                   # FastAPI backend calls
│   ├── config.py                    # API URL configuration
│   └── app.py                       # Main Streamlit entry point
│
└── server/                          # ⚙️ FastAPI Backend
    ├── middlewares/
    │   └── exception_handlers.py    # Global error handling
    ├── modules/
    │   ├── llm.py                   # Groq LLM + prompt template
    │   ├── load_vectorstore.py      # PDF → chunks → Pinecone
    │   └── query_handlers.py        # RAG query runner
    ├── routes/
    │   ├── upload_pdfs.py           # POST /upload_pdfs
    │   └── ask_question.py          # POST /ask
    ├── logs/
    │   └── app.log                  # Application logs
    ├── uploaded_docs/               # Temporary PDF storage
    ├── logger.py                    # Logger configuration
    ├── main.py                      # FastAPI app entry point
    └── requirements.txt             # Python dependencies
```

---

## 🔄 RAG Pipeline

```
                        ┌─────────────────────────────┐
                        │        USER UPLOADS PDF      │
                        └────────────┬────────────────┘
                                     │
                              PyPDFLoader
                                     │
                        RecursiveCharacterTextSplitter
                         (chunk_size=500, overlap=100)
                                     │
                        HuggingFace Embeddings
                         (all-mpnet-base-v2 → 768d)
                                     │
                        ┌────────────▼────────────────┐
                        │        PINECONE INDEX        │
                        └────────────────────────────-┘

                        ┌─────────────────────────────┐
                        │       USER ASKS QUESTION     │
                        └────────────┬────────────────┘
                                     │
                        Embed question (HuggingFace)
                                     │
                        Pinecone similarity search
                         (top_k = 3 documents)
                                     │
                        Build context from chunks
                                     │
                        Groq LLM (llama-3.3-70b)
                         + MediBot Prompt Template
                                     │
                        ┌────────────▼────────────────┐
                        │    ANSWER + SOURCES RETURNED │
                        └─────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Pinecone account → [app.pinecone.io](https://app.pinecone.io)
- Groq API key → [console.groq.com](https://console.groq.com)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/doctorassistant.git
cd doctorassistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the `server/` folder:

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medicalindex
```

### 5. Run the Backend

```bash
cd server
uvicorn main:app --reload
```

Backend runs at → `http://127.0.0.1:8000`  
Swagger docs at → `http://127.0.0.1:8000/docs`

### 6. Run the Frontend

Open a new terminal:

```bash
cd client
pip install streamlit
streamlit run app.py
```

Frontend runs at → `http://localhost:8501`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/upload_pdfs` | Upload one or more PDF files |
| `POST` | `/ask` | Ask a question about uploaded documents |

### Example — Upload PDF

```bash
curl -X POST http://127.0.0.1:8000/upload_pdfs \
  -F "files=@diabetes_guide.pdf"
```

### Example — Ask Question

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -F "question=What are the symptoms of diabetes?"
```

### Example Response

```json
{
  "response": "Common symptoms of diabetes include frequent urination, excessive thirst, unexplained weight loss, and blurred vision...",
  "sources": [
    "uploaded_docs/DIABETES.pdf",
    "uploaded_docs/DIABETES.pdf"
  ]
}
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq API key for LLM |
| `PINECONE_API_KEY` | ✅ | Pinecone vector DB key |
| `PINECONE_INDEX_NAME` | ✅ | Pinecone index name (e.g. `medicalindex`) |

---

## 📦 Requirements

```txt
fastapi
uvicorn
langchain==0.3.0
langchain-community==0.3.0
langchain-core==0.3.0
langchain-groq==0.2.0
langchain-huggingface
langchain-text-splitters==0.3.0
sentence-transformers
pinecone-client
python-dotenv
pypdf
streamlit
requests
```

---

## 🗺️ Roadmap

- [x] PDF ingestion and chunking
- [x] Vector storage with Pinecone
- [x] RAG pipeline with LangChain
- [x] Groq LLM integration
- [x] FastAPI REST backend
- [x] Streamlit chat UI
- [x] Download chat history
- [x] Structured logging
- [ ] User authentication
- [ ] Multi-language support
- [ ] Docker deployment
- [ ] Support for DOCX and TXT files
- [ ] Redis session management
- [ ] Deploy to AWS / Railway

---


## 👨‍💻 Author

Built with ❤️ by **Mohammad Affan**

[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/affanmohd65)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/mohammadaffan1/)

---

> 💡 **Tip:** Star ⭐ this repository if you found it helpful!

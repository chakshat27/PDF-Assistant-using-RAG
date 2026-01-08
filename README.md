# 📄 PDF Chat Assistant (FastAPI + LangChain + Groq)

An intelligent **PDF Question–Answering & Summarization web application** built using **FastAPI**, **LangChain**, **FAISS**, **BM25**, and **Groq LLM**.  
Users can upload PDFs, ask natural language questions, and receive **accurate, streamed answers** grounded strictly in the document content.

---

## 🚀 Features

- 📂 Upload PDF, DOCX, TXT, or Markdown files
- 🔍 Hybrid Retrieval:
  - FAISS (semantic search)
  - BM25 (keyword-based search)
- 🧠 Context-aware LLM responses using Groq
- ⚡ Streaming answers (real-time output)
- 🧩 Adaptive chunking based on document size
- 🎯 Query-focused summaries
- 🖥️ Clean HTML UI with Jinja templates

---

## 🛠️ Tech Stack

| Component | Technology |
|--------|------------|
| Backend | FastAPI |
| LLM | Groq |
| Retrieval | FAISS + BM25 |
| Text Processing | LangChain |
| Frontend | HTML, CSS, JS (Jinja2) |
| Streaming | FastAPI StreamingResponse |

---

## 📁 Project Architecture

FastAPI
├── File Upload
├── Background Chunking
├── Hybrid Retriever Creation
├── Query Processing
├── Streaming LLM Response




---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/pdf-chat-assistant.git
cd pdf-chat-assistant
```

### 2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate


### 3️⃣ Install Dependencies
pip install -r requirements.txt


### 4️⃣ Configure Environment Variables
# Add your Groq API key inside .env


### ▶️ Run the Application
``` uvicorn app:app --reload ```



🧪 Usage Flow

Upload a document (PDF/DOCX/TXT)

Wait for background processing

Enter your query

Get live streamed answers

Ask follow-up questions on the same document


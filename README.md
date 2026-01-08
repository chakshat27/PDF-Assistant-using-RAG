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


Here’s a **cleaned, more professional, and GitHub-ready README.md** that reads like a **serious production / portfolio project**, while still staying simple and crisp.
I’ve improved **clarity, structure, tone, formatting, and flow** without over-engineering it.

You can **copy-paste this directly** as your `README.md`.

---

# 📄 PDF Chat Assistant

**FastAPI · LangChain · FAISS · BM25 · Groq**

An intelligent **document question–answering and summarization web application** that allows users to upload documents and interact with them using **natural language queries**.

The system uses a **hybrid retrieval approach (semantic + keyword search)** combined with **LLM-based reasoning** to generate **accurate, context-aware, and streamed responses** strictly grounded in the uploaded document.

---

## 🚀 Key Features

* 📂 Upload and process **PDF, DOCX, TXT, and Markdown** files
* 🔍 **Hybrid document retrieval**

  * **FAISS** for semantic similarity search
  * **BM25** for keyword-based relevance
* 🧠 Context-aware responses powered by **Groq LLM**
* ⚡ **Real-time streamed answers** using FastAPI streaming
* 🧩 **Adaptive text chunking** based on document length
* 🎯 Query-focused summaries and explanations
* 🔄 Follow-up questions on the same document
* 🖥️ Simple and clean UI built with **Jinja2 templates**

---

## 🛠️ Tech Stack

| Layer           | Technology                     |
| --------------- | ------------------------------ |
| Backend         | FastAPI                        |
| LLM             | Groq                           |
| Retrieval       | FAISS, BM25                    |
| Text Processing | LangChain                      |
| Frontend        | HTML, CSS, JavaScript (Jinja2) |
| Streaming       | FastAPI `StreamingResponse`    |

---

## 🧠 System Architecture

```
User
 └── Upload Document
       └── Background Processing
             ├── Text Extraction
             ├── Adaptive Chunking
             ├── FAISS Index Creation
             └── BM25 Index Creation
       └── User Query
             ├── Hybrid Retrieval
             ├── Context Filtering
             └── LLM Streaming Response
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pdf-chat-assistant.git
cd pdf-chat-assistant
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
uvicorn app:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000
```

---

## 🧪 Usage Flow

1. Upload a document (PDF / DOCX / TXT / MD)
2. Wait briefly while the document is processed in the background
3. Enter a natural language query
4. Receive **live streamed answers** grounded in the document
5. Ask **follow-up questions** without re-uploading the file

---

## 🔍 Retrieval Strategy

* Combines **semantic understanding** (FAISS) with **keyword precision** (BM25)
* Merges top results from both retrievers
* Cleans extracted text to remove:

  * Figure references
  * Table mentions
  * Section numbering
* Sends only the **most relevant chunks** to the LLM for efficiency and accuracy

---


* 🧹 Refactor the codebase into services
* 📊 Add performance & scalability notes

Just say the word 👍

from fastapi import FastAPI, Request, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pathlib import Path
import asyncio, os, time
import re
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from groq import Groq
from config import EMBEDDINGS_MODEL, DATA_DIR, TEMPLATES_DIR, GROQ_API_KEY, MODEL_NAME, CHUNK_LIMITS

from fastapi.staticfiles import StaticFiles


# --------------- FASTAPI SETUP ---------------
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------- GLOBAL STORES ---------------
retriever_store = {}
query_store = {}
summary_chunks_store = {}

# --------------- LLM CLIENT ------------------
client = Groq(api_key=GROQ_API_KEY)


# ---------------- HOME PAGE ------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("get_pdf.html", {"request": request})


# ---------------- UPLOAD HANDLER ------------------
@app.post("/get_pdf")
async def process_file(
    file_upload: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    os.makedirs(DATA_DIR, exist_ok=True)
    save_path = os.path.join(DATA_DIR, file_upload.filename)

    # Save uploaded file
    with open(save_path, "wb") as f:
        content = await file_upload.read()
        f.write(content)

    # 🔹 Clear old state for this file (if re-uploaded)
    file_name = file_upload.filename
    retriever_store.pop(file_name, None)
    query_store.pop(file_name, None)
    summary_chunks_store.pop(file_name, None)

    # Launch background retriever creation
    background_tasks.add_task(process_and_split, save_path)

    # Redirect to query input page
    return RedirectResponse(f"/get_user_query?file_name={file_upload.filename}", status_code=302)


# ---------------- QUERY INPUT PAGE ------------------
@app.get("/get_user_query", response_class=HTMLResponse)
def get_user_query(request: Request):
    file_name = request.query_params.get("file_name", "")
    return templates.TemplateResponse("get_query.html", {"request": request, "file_name": file_name})


# ---------------- QUERY SUBMISSION ------------------
@app.post("/get_user_query", response_class=HTMLResponse)
async def user_query(
    request: Request,
    query: str = Form(...),
    file_name: str = Form(...)
):
    print(f"[LOG] Query received for file: {file_name}")

    retrievers = retriever_store.get(file_name)
    query_store[file_name] = query

    if not retrievers:
        return {"error": "Retriever not ready yet. Please wait and try again."}

    faiss_retriever, bm25_retriever = retrievers

    faiss_docs = faiss_retriever.get_relevant_documents(query)
    bm25_docs = bm25_retriever.get_relevant_documents(query)
    chunks = [doc.page_content for doc in faiss_docs + bm25_docs]

    summary_chunks_store[file_name] = chunks

    return templates.TemplateResponse("result.html", {
        "request": request,
        "file_name": file_name,
        "query": query
    })


# ---------------- STREAM SUMMARY ------------------
@app.get("/stream_summary")
async def stream_summary(file_name: str):
    chunks = summary_chunks_store.get(file_name)
    if not chunks:
        return {"error": "No chunks found for this file."}

    query = query_store.get(file_name)
    if not query:
        return {"error": "Query not found. Please submit first."}

    summary = await gen_llm_summary(chunks, query)
    return summary


# ----------------- PROCESS AND SPLIT -----------------
def make_docs(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext in [".txt", ".md"]:
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    return loader.load()


async def process_and_split(file_path):
    docs = make_docs(file_path)
    total_pages = len(docs)

    # Adaptive chunking
    for limit, size, overlap in CHUNK_LIMITS:
        if total_pages <= limit:
            chunk_size, chunk_overlap = size, overlap
            break

    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(docs)
    filename = os.path.basename(file_path)

    faiss_retriever, bm25_retriever = await build_retrievers(chunks)
    retriever_store[filename] = (faiss_retriever, bm25_retriever)

    print(f"[LOG] Finished building retrievers for {filename}")


# ----------------- BUILD RETRIEVERS -----------------
async def build_retrievers(chunks):
    start = time.time()

    faiss_task = asyncio.to_thread(FAISS.from_documents, chunks, EMBEDDINGS_MODEL)
    bm25_task = asyncio.to_thread(BM25Retriever.from_documents, chunks)

    vectorstore, bm25_retriever = await asyncio.gather(faiss_task, bm25_task)

    print(f"[LOG] Vectorstore built in {time.time() - start:.2f}s")
    return vectorstore.as_retriever(search_kwargs={"k": 2}), bm25_retriever


# ----------------- LLM SUMMARY -----------------
async def gen_llm_summary(docs, query):
    # Combine limited chunks
    combined_text = " ".join(docs[:15])

    # 🔹 Clean unwanted patterns (figure refs, table mentions, etc.)
    patterns_to_remove = [
        r'Figure\s?\d+',
        r'Table\s?[IVXLC\d]+',
        r'Section\s?\d+',
        r'Algorithm\s?\d+',
        r'References',
        r'©\s?\d{4}',   # e.g., © 2023
    ]
    for pattern in patterns_to_remove:
        combined_text = re.sub(pattern, '', combined_text, flags=re.IGNORECASE)



    # summarization prompt
    prompt = f"""

You are an intelligent, context-aware assistant analyzing the text extracted from a PDF.

Step 1 — Carefully read the provided document text below.

Step 2 — Identify the user’s intent from the query: "{query}".
- If the query asks for a something specific, give a **direct and minimal answer** , drawn precisely from the document text.
- If the query asks for a **summary, explanation, or analysis**, 
  then provide a **comprehensive yet concise** explanation or overview that covers all key points clearly.

Step 3 — Keep your tone natural and human. 
Avoid mentioning figure numbers, section titles, or unrelated context. 
If there is insufficient detail to answer confidently, say so without guessing.

Do NOT include word counts, metadata, or any trailing symbols like "(≈115 words)".
There is no strict word limit, but prefer clarity and precision.

Content:
{combined_text}
"""
    




    # 🔹 Call LLM with stream
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        stream=True
    )

    async def generator():
        for chunk in completion:
            text = chunk.choices[0].delta.content or ""
            yield text

    return StreamingResponse(generator(), media_type="text/plain")





# ----------------- FOLLOW-UP QUERY -----------------
@app.get("/followup_query")
async def followup_query(file_name: str, query: str):
    retrievers = retriever_store.get(file_name)
    if not retrievers:
        return {"error": "Retriever not ready for this file."}

    faiss_retriever, bm25_retriever = retrievers

    faiss_docs = faiss_retriever.get_relevant_documents(query)
    bm25_docs = bm25_retriever.get_relevant_documents(query)
    chunks = [doc.page_content for doc in faiss_docs + bm25_docs]

    summary_chunks_store[file_name] = chunks  # optional — reuse for context

    # Stream summary like main query
    return await gen_llm_summary(chunks, query)



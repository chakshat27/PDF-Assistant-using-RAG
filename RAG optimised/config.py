# config.py
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load environment variables from .env file
load_dotenv()

# Embedding model for FAISS vector store
EMBEDDINGS_MODEL = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Directory paths
DATA_DIR = "./data/"
TEMPLATES_DIR = "templates/"

# LLM Configuration
# Pull GROQ_API_KEY from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "openai/gpt-oss-120b"

# Chunking configuration
CHUNK_LIMITS = [
    (20, 300, 50),
    (100, 450, 100),
    (200, 500, 100),
    (9999, 600, 150),
]

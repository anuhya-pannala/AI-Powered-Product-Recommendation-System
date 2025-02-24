import os
import sys
import chromadb
import faiss
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.db import get_list_products, get_list_ingrediants, get_engine
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
USE_OPENAI = os.getenv("USE_OPENAI", "False").lower() == "true"

DB_FILE = os.getenv("DB_PATH")
conn_engine = get_engine(DB_FILE)

embedding_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY) if USE_OPENAI else OllamaEmbeddings()

# FAISS Index File
FAISS_INDEX_FILE = "faiss_index"

def store_embeddings(engine):
    """Fetch product & ingredient data, convert to embeddings, and store in FAISS"""
    # Fetch products & ingredients data
    products = get_list_products(engine, mode="default")
    ingredients = get_list_ingrediants(engine, mode="default")

    # Prepare text data for embeddings
    documents = []
    for product in products:
        text = f"Product: {product['name']}, Description: {product['description']},\
            Ingredients: {product['ingredients']}, Effects: {product['effects']}"
        documents.append(text)

    for ingredient in ingredients:
        text = f"Ingredient: {ingredient['name']}, Properties: {ingredient['properties']},\
            Effects: {ingredient['common_effects']}"
        documents.append(text)


    # Split text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    final_documents = text_splitter.create_documents(documents)

    # Store embeddings in FAISS
    vector_store = FAISS.from_documents(final_documents, embedding_model)
    vector_store.save_local(FAISS_INDEX_FILE)

    print("Embeddings stored in FAISS")


if __name__ == "__main__":
    store_embeddings(conn_engine)

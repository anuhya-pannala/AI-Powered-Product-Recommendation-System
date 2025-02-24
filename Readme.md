# AI-Powered Product Recommendation System with RAG

## Description

We have successfully built a FastAPI-powered backend system for an AI-driven product recommendation and augmentation system using SQLite, FAISS, LangChain, and OpenAI/Groq LLMs. Below is a structured breakdown of everything we have done so far.

## Technologies/Tools Used

- **Python (FastAPI)**: Server and API management.
- **SQLite**: Database for storing product data.
- **SQLAlchemy**: Database toolkit and ORM.
- **FAISS**: High performance similarity search and clustering of dense vectors.
- **LangChain**: Integration of language models in applications.
- **OpenAI/Groq LLMs**: Utilized for generating responses and augmenting content.

## Steps to Run the Backend Application

1. **Go to the Backend Folder**

   ```bash
   cd Backend
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**

   ```bash
   venv/Scripts/activate
   ```

4. **Upgrade pip**

   ```bash
   python -m pip install --upgrade pip
   ```

5. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

6. **Initialize Database**

   ```bash
   # This script reads mock data and creates a database, storing the info.
   python src/db.py
   ```

7. **Create Vector Database**

   ```bash
   # This script creates a vector database and stores it in a file.
   python src/vector_store.py
   ```

8. **Start the FastAPI Server**

   ```bash
   uvicorn src.main:app --reload
   ```

9. **Deactivate Virtual Environment When Done**
   ```bash
   deactivate
   ```

## API Endpoints

| Endpoint                                    | Purpose                                      |
| ------------------------------------------- | -------------------------------------------- |
| `/`                                         | Basic API health check                       |
| `/products`                                 | Retrieve all products                        |
| `/products/{product_id}`                    | Get details of a specific product            |
| `/sales`                                    | Retrieve all sales data                      |
| `/sales/{product_id}`                       | Get sales data for a specific product        |
| `/get_content_recommendations/{product_id}` | Get content-based product recommendations    |
| `/rag-query/?query=XYZ`                     | Answer any user query using RAG              |
| `/augment/?product_name=XYZ`                | Generate an AI-augmented product description |




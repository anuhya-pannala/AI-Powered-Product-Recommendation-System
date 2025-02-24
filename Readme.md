# AI-Powered Product Recommendation System with RAG

## Description

Successfully built a FastAPI-powered backend system for an AI-driven product recommendation and augmentation system using SQLite, FAISS, LangChain, and OpenAI/Groq LLMs. Below is a structured breakdown of everything done so far.

## Technologies/Tools Used

- **Python (FastAPI)**: Server and API management.
- **SQLite**: Database for storing product data.
- **FAISS**: High performance similarity search and clustering of dense vectors.
- **LangChain**: Integration of language models in applications.
- **OpenAI/Groq LLMs**: Utilized for generating responses and augmenting content.

## Steps to Run the Frontend and Backend Application
- Frontend:
1. **Go to the Frontend Folder**
      ```bash
   cd frontend
   ```
2. **Start the server**
   ```bash
   npm start
   ```
In a different terminal:
- Backend
1. **Go to the Backend Folder**

   ```bash
   cd backend
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



# Overview

This project is an AI-powered product recommendation system that leverages content-based filtering and Retrieval-Augmented Generation (RAG) to provide intelligent product recommendations. The system is built using FastAPI for the backend, FAISS for vector-based retrieval, and OpenAI/Groq LLMs for generating enhanced product descriptions.

## Assumptions and Simplifications

1. Sales data is not used for content-based filtering or product recommendations, as sales do not directly influence similarity-based recommendations.

2. FAISS was chosen over ChromaDB for vector storage due to its efficiency in handling large-scale similarity searches.

3. Collaborative filtering is not implemented since we lack user-specific transaction or interaction data.

4. Only product and ingredient data are stored in the vector database, as they provide meaningful context for recommendations.

## Approach

Recommendation Algorithm

1. The system fetches all products from the database and vectorizes product descriptions, effects, and ingredients using TF-IDF (Term Frequency-Inverse Document Frequency).

2. Using cosine similarity, the algorithm determines top-N most similar products for a given product ID.

3. The top-N recommendations are returned as a ranked list of similar products.

Retrieval-Augmented Generation (RAG) Implementation

1. Product and ingredient data are embedded using FAISS and stored for efficient retrieval.

2. A retriever extracts relevant context based on user queries using FAISS.

3. The LLM (OpenAI/Groq) takes the retrieved context and generates an AI-powered response.

4. The system provides two RAG-powered features:

- Answering user queries related to product benefits and details.

- Generating augmented product descriptions based on the retrieved context.

## Potential Areas for Improvement

1. Collaborative Filtering: If user transaction data is available, we can implement collaborative filtering to enhance recommendations based on user behavior.

2. User Chat History: Storing past user queries can help refine recommendations based on previous interactions.

3. Hybrid Recommendation System: Combining content-based filtering with collaborative filtering to improve accuracy and personalization.

34. Real-time Embedding Updates: Implementing a pipeline to dynamically update FAISS embeddings as new products are added.

## Tech Stack

- Backend: FastAPI, Python

- Database: SQLite, SQLAlchemy

- Vector Search: FAISS

- ML/AI: OpenAI API, Groq API, LangChain

- Recommendation: TF-IDF, Cosine Similarity


## Conclusion

This project showcases a scalable and intelligent recommendation system that leverages both traditional ML techniques (TF-IDF) and modern LLM-powered RAG to enhance product discovery. With further improvements, such as collaborative filtering and user-based recommendations, this system can evolve into a fully personalized recommendation engine for e-commerce platforms.




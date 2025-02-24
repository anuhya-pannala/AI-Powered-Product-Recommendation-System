"""Fast API file"""
import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.db import get_engine, fetch_table_data, get_product_details_by_id
from src.db import get_list_products
from src.recommendation_service import recommend_products
from src.rag import retrieve_and_generate, generate_augmented_description
from dotenv import load_dotenv
load_dotenv()

# Configure Logging
# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG, force=True)
# logger = logging.getLogger(__name__)

# Configure Logging (force stdout)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True
)

logger = logging.getLogger(__name__)

# logger = logging.getLogger('uvicorn.error')
# logger.setLevel(logging.DEBUG)

app = FastAPI()

# ✅ CORS Configuration (Allow frontend to call the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to frontend's URL for security (e.g., "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Database Engine
DB_FILE = os.getenv("DB_PATH")
engine = get_engine(DB_FILE)

@app.get("/products")
def get_products():
    """Fetch all products from the database"""
    logger.debug("Inside /products endpoint")
    print("Inside /products endpoint - print()")
    # products = fetch_table_data("products", engine, mode="default")
    products = get_list_products(engine, mode="default")
    # print(products.head())
    return {"products": products}

@app.get("/")
def read_root():
    """Sample api"""
    logger.info("Inside / endpoint")
    # print("Inside / endpoint - print()")
    return {"message": "Hello, BakedBot!"}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Fetch a single product by ID directly from the database"""
    # logger.info("Inside get products by id")
    product = get_product_details_by_id(engine, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"product": product}

# @app.get("/sales")
# def get_sales():
#     """Fetch all sales data"""
#     sales = fetch_table_data("sales", engine, mode="default")

#     if not sales:
#         raise HTTPException(status_code=404, detail="No sales data found")

#     return {"sales": sales}

# @app.get("/sales/{product_id}")
# def get_sales_by_prod(product_id: int):
#     """Fetch all sales data"""
#     sales = get_sales_data_by_prod(engine, product_id)

#     if not sales:
#         raise HTTPException(status_code=404, detail="No sales data found")

#     return {"sales": sales}


@app.get("/get_content_recommendations/{product_id}")
def get_content_recommendations(product_id: int):
    """Get recommendations using TF-IDF"""
    print("In get recommend api")
    res = recommend_products(engine, product_id, top_n=5)

    if not res:
        raise HTTPException(status_code=404, detail="No recommendation data found")

    return {"recommendation": res}

@app.get("/rag-query/")
def get_rag_response(query: str):
    """Retrieve information using RAG and return AI-generated response"""
    response = retrieve_and_generate(query)
    return {"response": response}

@app.get("/augment/")
def get_augmented_description(product_name: str):
    """Augment product description using RAG and return AI-generated response"""
    print(product_name)
    response = generate_augmented_description(product_name)
    return {"response": response}

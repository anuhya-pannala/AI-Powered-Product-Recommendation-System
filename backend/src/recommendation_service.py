"""File to handle recommendation features"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.db import get_list_products, get_engine

def recommend_products(engine, product_id, top_n=3):
    """Recommend similar products based on product descriptions and effects"""

    # Fetch all products using fetch_table_data()
    print(f"Inside recommendations for product {product_id}")
    # products = fetch_table_data("products", engine, mode="default")

    products = get_list_products(engine, mode="default")

    if not products:
        return None

    # Create a combined text column (description + effects)
    product_texts = [f"{p['description']} {p['effects']} {p['ingredients']}" for p in products]

    # Convert text data to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(product_texts)

    # Get index of the input product
    product_index = next((i for i, p in enumerate(products) if p["id"] == product_id), None)
    if product_index is None:
        return None  # Product ID not found

    # Compute cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix[product_index], tfidf_matrix).flatten()

    # Get top N similar product indices (excluding itself)
    similar_indices = similarity_scores.argsort()[-(top_n+1):-1][::-1]

    # Get recommended products
    recommendations = [{"id": products[i]["id"],
                        "name": products[i]["name"], 
                        "score": float(similarity_scores[i])} for i in similar_indices]

    return recommendations if recommendations else None


# if __name__ == "__main__":
#     DB_FILE = "sqlite:///D:/Study/Projects/BakedBot/baked_bot/backend/bakedbot.db"
#     conn_engine = get_engine(DB_FILE)
#     res = recommend_products(conn_engine, 1, top_n=5)
#     print(res)

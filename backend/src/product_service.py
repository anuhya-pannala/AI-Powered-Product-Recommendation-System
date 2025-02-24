"""Product service file."""
import json

def get_products():
    """Get product details"""
    with open("products.json", "r", encoding="utf-8") as file:
        products = json.load(file)
    return {"products": products}

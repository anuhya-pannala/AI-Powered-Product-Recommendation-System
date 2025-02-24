import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import "./ProductPage.css"; // Import styles
import Chatbot from "./Chatbot"; // Import the Chatbot component

const ProductPage = () => {
  const { productId } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [augmentedDescription, setAugmentedDescription] = useState("");
  const [recommendedProducts, setRecommendedProducts] = useState([]);


  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/products/${productId}`)
      .then(response => {
        if (response.data?.product) setProduct(response.data.product);
      })
      .catch(error => console.error("Error fetching product details:", error));
  }, [productId]);

  useEffect(() => {
    if (product?.name) {
      axios.get(`http://127.0.0.1:8000/augment/?product_name=${encodeURIComponent(product.name)}`)
        .then(response => setAugmentedDescription(response.data.response || "No AI-Enhanced description available."))
        .catch(() => setAugmentedDescription("Failed to fetch AI-enhanced description."));
    }
  }, [product?.name]);

  useEffect(() => {
    if (product?.id) {
      axios.get(`http://127.0.0.1:8000/get_content_recommendations/${product.id}`)
        .then(response => setRecommendedProducts(response.data.recommendation || []))
        .catch(() => setRecommendedProducts([]));

    }
  }, [product?.id]);

  return (
    <div className="product-container">
      <button className="back-btn" onClick={() => navigate("/")}>⬅Back to the List</button>

      <div className="content">

        <div className="product-details">
          {product ? (
            <>
              <h1>{product.name}</h1>
              <p className="desc">{product.description || "No description available."}</p>
              <p className="price"><strong>Price:</strong> {product.price ? `$${product.price.toFixed(2)}` : "Not available"}</p>

              <div className="section">
                <h2>✨ AI-Enhanced Description</h2>
                <p>{augmentedDescription || "Loading..."}</p>
              </div>
            </>
          ) : <p className="loading">🔄 Loading product details...</p>}
        </div>

        <div className="recommendations">
          <h2>💡 Recommended Products</h2>
          {recommendedProducts.length > 0 ? (
            <ul>
              {recommendedProducts.map(rec => (
                <li key={rec.id}>{rec.name} (Matching: {(rec.score * 100).toFixed(2)}%)</li>
              ))}
            </ul>
          ) : <p>No recommendations available.</p>}
        </div>
      </div>
      {/* Render the chatbot component */}
      <Chatbot />
    </div>
  );
};

export default ProductPage;

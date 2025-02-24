import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Chatbot from "./Chatbot"; // Import the Chatbot component
import "./Home.css"; // Import your existing CSS

const Home = () => {
  const [products, setProducts] = useState([]);
  const navigate = useNavigate(); // Use navigate hook to change pages

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/products")
      .then((response) => setProducts(response.data.products))
      .catch((error) => console.error("Error fetching products:", error));
  }, []);

  return (
    <div className="container">
      <h1 className="heading">🛍️ Explore Our Products</h1>
      
      <div className="product-grid">
        {products.length > 0 ? (
          products.map((product) => (
            <div
              key={product.id}
              className="product-card"
              onClick={() => navigate(`/products/${product.id}`)}
            >
              <h3 className="product-title">{product.name}</h3>
            </div>
          ))
        ) : (
          <p>Loading products...</p>
        )}
      </div>

      {/* Render the chatbot component */}
      <Chatbot />
    </div>
  );
};

export default Home;

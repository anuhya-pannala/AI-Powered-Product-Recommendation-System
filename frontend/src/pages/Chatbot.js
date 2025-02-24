import React, { useState } from "react";
import axios from "axios";
import "./Chatbot.css"; // Import CSS for styling

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [userMessage, setUserMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userMessage.trim()) return;

    // user's message to chat history
    setChatHistory((prev) => [
      ...prev,
      { sender: "user", message: userMessage },
    ]);

    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/rag-query/?query=${encodeURIComponent(
          userMessage
        )}`
      );

      // bot's response to chat history
      if (response.data && response.data.response) {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", message: response.data.response },
        ]);
      } else {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", message: "Sorry, no response available." },
        ]);
      }
    } catch (error) {
      console.error("Error fetching chatbot response", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", message: "Error fetching response." },
      ]);
    }
    setUserMessage("");
  };

  return (
    <>
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <span>Chatbot</span>
            <button className="chatbot-close" onClick={toggleChat}>
              X
            </button>
          </div>
          <div className="chatbot-body">
            {chatHistory.length === 0 ? (
              <p className="chatbot-message">Hello! How can I help you today?</p>
            ) : (
              chatHistory.map((chat, index) => (
                <div
                  key={index}
                  className={`chat-message ${chat.sender}`}
                >
                  {chat.message}
                </div>
              ))
            )}
          </div>
          <form onSubmit={handleSubmit} className="chatbot-form">
            <input
              type="text"
              placeholder="Type your message..."
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              className="chatbot-input"
            />
            <button type="submit" className="chatbot-send">
              Send
            </button>
          </form>
        </div>
      )}
      <button className="chatbot-toggle" onClick={toggleChat}>
        <img
          src="https://img.icons8.com/ios-filled/50/ffffff/chat--v1.png"
          alt="Chatbot Icon"
        />
      </button>
    </>
  );
};

export default Chatbot;

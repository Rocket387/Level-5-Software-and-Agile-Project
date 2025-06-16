import React, { useState } from 'react';
import './chatbot.css'; 
import { chatbotSend } from '../api';  


function ChatBot() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;
    try {
      const res = await chatbotSend(input);
      setMessages([...messages, { from: 'user', text: input }, { from: 'bot', text: res.data.response }]);
      setInput("");
    } catch (error) {
      console.error("Error sending message", error);
      setMessages([...messages, { from: 'user', text: input }, { from: 'bot', text: "Oops! Something went wrong." }]);
      setInput("");
    }
  };

  const handleToggle = () => {
    setOpen(!open);
    if (!open) {
      // Add a greeting message when the chatbot is opened
      setMessages([
        { from: 'bot', text: "Hello, I'm Suru, your PV team chatbot! Please enter your question or web link and I will do my best to assist you..." }
      ]);
    }
  };

  return (
    <>
      {/* Chatbot Toggle Button */}
      <button
        className="chatbot-toggle"
        onClick={handleToggle}
      >
        💬
      </button>

      {/* Chatbot Container */}
      {open && (
        <div className="chatbot-container">
          <div className="chatbot-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`chatbot-message ${msg.from}`}>
                {msg.text}
              </div>
            ))}
          </div>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type a message..."
          />
        </div>
      )}
    </>
  );
}

export default ChatBot;

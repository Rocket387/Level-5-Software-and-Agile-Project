import React, { useState } from 'react';
import axios from 'axios';
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

  return (
    <>
      {/* Chatbot Toggle Button */}
      <button
        className="chatbot-toggle"
        onClick={() => setOpen(!open)}
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

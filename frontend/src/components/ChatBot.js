import React, { useState } from "react";
import "../styles/style.css";

const ChatBot = () => {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (input.trim() === "") return;

    // Append user message
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      setMessages([...newMessages, { sender: "bot", text: data.response }]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: "bot", text: "Error contacting server." },
      ]);
    }

    setInput("");
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={msg.sender === "user" ? "user-msg" : "bot-msg"}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatBot;

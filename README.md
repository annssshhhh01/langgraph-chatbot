# Agentic Chatbot | LangGraph + FastAPI + React

A full-stack AI orchestration engine demonstrating **Agentic AI** workflows. This project uses **LangGraph** to manage stateful, multi-turn conversations with persistent memory and **Llama 3.3** for high-reasoning capabilities.

---

## Key Features
* **Stateful Memory:** Uses `InMemorySaver` and `thread_id` to persist chat history across sessions.
* **Agentic Orchestration:** Built with **LangGraph** for robust control over message flow and state transitions.
* **FastAPI Backend:** High-performance Python API with Pydantic validation and CORS-ready middleware.
* **Modern UI:** Dark-themed, mobile-responsive React frontend built with **Vite**.
* **Optimized LLM:** Powered by **Groq (Llama-3.3-70b-versatile)** for near-instant responses.

##  Tech Stack
| Component | Technology |
| :--- | :--- |
| **AI Framework** | LangGraph, LangChain |
| **LLM Provider** | Groq (Llama 3.3) |
| **Backend** | Python, FastAPI, Uvicorn |
| **Frontend** | React.js, Vite, CSS3 |
| **Persistence** | LangGraph InMemorySaver |

---

## Project Structure
```text
chatbot2/
├── backend/
│   ├── api.py               # FastAPI Endpoints & CORS
│   ├── langgraph_python.py  # LangGraph Logic & Node Definitions
│   └── __init__.py
├── chatbot/                 # React Frontend Folder
│   ├── src/
│   │   ├── App.jsx          # Chat UI & Fetch Logic
│   │   └── App.css          # Modern Dark-Theme Styles
├── .env                     # API Keys (Excluded)
└── README.md




```


-> Setup & Installation
1. Backend Setup
Navigate to backend: cd backend

Install dependencies:
```
pip install fastapi uvicorn langgraph langchain_groq python-dotenv
```
Configure environment: Create a .env file in the root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run Server:
```
python -m uvicorn api:app --reload
```

2. Frontend Setup
Navigate to chatbot:
```
 cd chatbot
```
Install & Run:
````
npm install
npm run dev
```

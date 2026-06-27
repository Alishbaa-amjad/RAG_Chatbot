# 🤖 NETSOL AI RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) Chatbot developed during my internship at **NETSOL Technologies**. This chatbot answers user queries about NETSOL Technologies by retrieving relevant information from a custom knowledge base and generating accurate, context-aware responses using Google Gemini.

---

## 📌 Overview

This project implements a complete **Retrieval-Augmented Generation (RAG)** pipeline.

Instead of relying solely on a Large Language Model, the chatbot first retrieves relevant information from a vector database and then generates responses using Google's Gemini model.

The application follows a modular architecture consisting of a React frontend, FastAPI backend, LangGraph workflow, semantic search, and an automated web scraping pipeline.

---

## ✨ Features

- 🤖 AI-powered chatbot
- 🔍 Semantic search using FAISS
- 🧠 Google Gemini integration
- 🔄 LangGraph workflow orchestration
- 🌐 Automated website scraping
- 📚 Source-aware responses
- ⚡ FastAPI REST API
- 💻 Responsive React frontend
- 🗄 SQLite database
- 🛡 Error handling and fallback mechanism

---

# 🛠 Tech Stack

### Backend
- Python
- FastAPI
- LangGraph
- Google Gemini API
- FAISS
- Sentence Transformers
- SQLite

### Frontend
- React.js

### Web Scraping
- Selenium
- BeautifulSoup
- Requests

---

# 📂 Project Structure

```
CHATBOT_ALISHBA/

│── backend/
│   ├── data/
│   ├── graph/
│   ├── llm/
│   ├── pipeline/
│   ├── retrieval/
│   ├── scraper/
│   ├── .env
│   ├── main.py
│   └── requirements.txt
│
│── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
│
├── README.md
└── .gitignore
```

---

# ⚙️ How It Works

### Step 1
Scrape website data using Selenium.

### Step 2
Clean and preprocess the extracted content.

### Step 3
Split the content into smaller chunks.

### Step 4
Generate vector embeddings using Sentence Transformers.

### Step 5
Store embeddings in FAISS.

### Step 6
Retrieve relevant chunks according to the user's question.

### Step 7
LangGraph manages the AI workflow.

### Step 8
Google Gemini generates the final response.

### Step 9
Display the response with source references.

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/CHATBOT_ALISHBA.git

cd CHATBOT_ALISHBA
```

---

## Backend Setup

```bash
cd backend

python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Backend

```bash
uvicorn main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm start
```

---

# 📊 Workflow Diagram

```
              User
                │
                ▼
         React Frontend
                │
                ▼
          FastAPI Backend
                │
                ▼
          LangGraph Graph
                │
      ┌─────────┴─────────┐
      │                   │
Retrieve Documents     Handle Errors
      │
      ▼
     FAISS
      │
      ▼
Relevant Chunks
      │
      ▼
 Google Gemini
      │
      ▼
 Generated Answer
      │
      ▼
 React Frontend
```

---

# 📚 Technologies Used

- Python
- FastAPI
- React.js
- LangGraph
- Google Gemini
- FAISS
- Sentence Transformers
- Selenium
- BeautifulSoup
- Requests
- SQLite

---

# 🎯 Learning Outcomes

This project helped me gain hands-on experience in:

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- LangGraph
- Semantic Search
- Vector Embeddings
- FAISS Vector Database
- Full Stack Development
- REST APIs
- Web Scraping
- Prompt Engineering
- AI Workflow Design

---

# 🙏 Acknowledgements

Developed during my internship at **NETSOL Technologies**.

Special thanks to:

- Sir Muneeb
- Sir Waqas
- Mr. Saleem Ghauri
- The entire NETSOL Technologies team

for their guidance, mentorship, and continuous support throughout this project.

---

# 👩‍💻 Author

**Alishba Amjad**

GitHub: https://github.com/alishbaa-amjad

LinkedIn: www.linkedin.com/in/alishbaa-amjad

---

# ⭐ Support

If you found this project useful, don't forget to ⭐ the repository.

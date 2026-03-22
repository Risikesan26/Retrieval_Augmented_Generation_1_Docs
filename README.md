# DocChat — RAG-Powered Document Q&A

A Retrieval-Augmented Generation (RAG) app that lets you upload PDF documents and ask questions about them using natural language.

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | [Groq](https://groq.com) — `llama-3.3-70b-versatile` |
| Embeddings | [Cohere](https://cohere.com/) — `embed-english-v3.0` |
| Vector DB | [ChromaDB](https://www.trychroma.com) |
| Backend | [FastAPI](https://fastapi.tiangolo.com) |
| Frontend | [Streamlit](https://streamlit.io) |

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running
- A [Groq](https://console.groq.com) API key (free)

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Pull the embedding model

```bash
ollama pull nomic-embed-text
```

### 4. Set up environment variables

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Running the App

Open **two terminals**:

**Terminal 1 — Start the FastAPI backend:**
```bash
uvicorn main:app --reload
```
API runs at `http://127.0.0.1:8000`

**Terminal 2 — Start the Streamlit frontend:**
```bash
streamlit run app_ui.py
```
UI runs at `http://localhost:8501`

---

## Usage

1. Open `http://localhost:8501` in your browser
2. Upload a PDF in the sidebar — it gets indexed automatically
3. Type your question in the chat box
4. Toggle **Show source context** to see which parts of the document were used

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload and index a PDF |
| `POST` | `/ask?question=...` | Ask a question |

Interactive docs available at `http://127.0.0.1:8000/docs`

---

## Project Structure

```
├── main.py          # FastAPI backend
├── app_ui.py        # Streamlit frontend
├── requirements.txt
├── .env             # API keys (never commit this)
├── .gitignore
└── chroma_db/       # Auto-created vector database
```

---

## Notes

- Delete the `chroma_db/` folder if you switch embedding models
- Ollama must be running locally for embeddings to work
- Free Groq tier is sufficient for most use cases

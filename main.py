from fastapi import FastAPI, UploadFile, File, HTTPException
import chromadb
import pdfplumber
import cohere
import io
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

# =========================
# CONFIG
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Set GROQ_API_KEY in environment variables")
if not COHERE_API_KEY:
    raise ValueError("Set COHERE_API_KEY in environment variables")

# Groq client — LLM only
groq_client = Groq(api_key=GROQ_API_KEY)

# Cohere client — embeddings only
co = cohere.ClientV2(COHERE_API_KEY)

# ✅ Fixed Chroma client
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection("documents_v2")

app = FastAPI(title="RAG API (Groq + Cohere)")

# =========================
# PDF TEXT EXTRACTION
# =========================
def extract_text_from_pdf(file_bytes: bytes) -> list[str]:
    chunks = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
                for para in paragraphs:
                    chunks.append(f"[Page {page_num+1}] {para}")
    return chunks

# =========================
# EMBEDDINGS (Cohere)
# =========================
def get_embeddings(texts: list[str], input_type: str = "search_document") -> list[list[float]]:
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type=input_type,
        embedding_types=["float"]
    )
    # ✅ Safe extraction
    return [list(e) for e in response.embeddings.float_]

# =========================
# UPLOAD PDF
# =========================
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # ✅ Check content type too, not just filename
    if not file.filename.endswith(".pdf") and file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    chunks = extract_text_from_pdf(content)
    if not chunks:
        raise HTTPException(status_code=400, detail="No text found in PDF")

    embeddings = get_embeddings(chunks, input_type="search_document")
    ids = [f"{file.filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": file.filename, "chunk_id": i} for i in range(len(chunks))]

    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)

    return {"message": f"Indexed {len(chunks)} chunks from {file.filename}"}

# =========================
# ASK QUESTION
# =========================
@app.post("/ask")
async def ask_question(question: str):
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    q_embedding = get_embeddings([question], input_type="search_query")[0]

    results = collection.query(query_embeddings=[q_embedding], n_results=3)
    if not results["documents"] or not results["documents"][0]:
        return {"answer": "No relevant documents found."}

    context = "\n\n".join(results["documents"][0])

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You answer strictly using provided context."},
            {"role": "user", "content": f"""
Answer ONLY using the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""}
        ],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=False
    )

    answer = response.choices[0].message.content
    return {"answer": answer, "context_used": results["documents"][0]}

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "RAG API running with Cohere embeddings + Groq LLM 🚀"}

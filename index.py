
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.pdf_processor import extract_pdf_text
from services.chunking import split_into_chunks
from services.database import supabase
from services.embedding import get_embeddings
from services.retrieval import retrieve_documents
from services.generation import generate_answer


app = FastAPI(
    title="Document Intelligence Assistant",
    description="RAG-based document question-answering system",
    version="1.1.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ChatRequest(BaseModel):
    question: str
    document_id: str


@app.get("/")
def home():
    return {
        "message": "Document Intelligence Assistant API is running!",
        "status": "success"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# PDF upload
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB."
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF document."
        )

    try:
        extracted_text = extract_pdf_text(content)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF."
            )

        chunks = split_into_chunks(extracted_text)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No readable text chunks found."
            )

        document_response = (
            supabase.table("documents")
            .insert({"filename": file.filename})
            .execute()
        )

        document_id = document_response.data[0]["id"]

        embeddings = get_embeddings(chunks)

        chunk_records = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            chunk_records.append({
                "document_id": document_id,
                "chunk_index": index,
                "content": chunk,
                "embedding": embedding
            })

        batch_size = 100

        for start in range(0, len(chunk_records), batch_size):
            batch = chunk_records[start:start + batch_size]

            supabase.table(
                "document_chunks"
            ).insert(batch).execute()

        return {
            "filename": file.filename,
            "status": "success",
            "message": "PDF uploaded and stored successfully!",
            "document_id": document_id,
            "total_characters": len(extracted_text),
            "total_chunks": len(chunks),
            "stored_embeddings": len(embeddings)
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}"
        )


# RAG chat with source references
@app.post("/chat")
def chat_with_document(request: ChatRequest):

    try:
        chunks = retrieve_documents(
            request.question,
            document_id=request.document_id
        )

        answer = generate_answer(
            request.question,
            chunks
        )

        # Prepare source references
        sources = []

        for index, chunk in enumerate(chunks, start=1):
            sources.append({
                "source_number": index,
                "content": chunk["content"],
                "similarity": round(
                    float(chunk["similarity"]), 4
                )
            })

        return {
            "status": "success",
            "question": request.question,
            "answer": answer,
            "retrieved_chunks": len(chunks),
            "sources": sources
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(error)}"
        )

# Document Intelligence Assistant

A RAG-based web application for asking questions about uploaded PDF documents.

## Current scaffold

- FastAPI starter API
- PDF text extraction helper
- Text chunking helper
- Placeholder modules for embeddings, retrieval, and answer generation
- Starter web interface

## Local setup (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m uvicorn api.index:app --reload
```

Open http://127.0.0.1:8000/ for the API response and
http://127.0.0.1:8000/docs for interactive API documentation.

The frontend in `public/` is a starter screen and is not yet connected to the API.
We will connect it in the implementation stages.

## Environment variables

Copy `.env.example` to `.env` and fill in your own API credentials when we configure
Gemini, Groq, and Supabase. Never commit `.env` to GitHub.

## Deployment

Vercel configuration and production routes will be added after local functionality
is implemented and tested.

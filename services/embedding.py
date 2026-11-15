
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_embedding(text, task_type="RETRIEVAL_DOCUMENT"):

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    client = genai.Client(api_key=GEMINI_API_KEY)

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values


def get_embeddings(texts):
    return [
        get_embedding(text, "RETRIEVAL_DOCUMENT")
        for text in texts
    ]

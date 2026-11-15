import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_answer(question, retrieved_chunks):

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from .env")

    if not retrieved_chunks:
        return "I could not find relevant information in your uploaded documents."

    # Prepare context from retrieved document chunks
    context = "\n\n".join(
        chunk["content"] for chunk in retrieved_chunks
    )

    # Initialize Groq client
    client = Groq(api_key=GROQ_API_KEY)

    # Generate answer using retrieved context
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Document Intelligence Assistant. "
                    "Answer questions using only the provided document context. "
                    "If the answer is not available in the context, "
                    "clearly say that the document does not provide the answer. "
                    "Do not invent information."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Document Context:\n{context}\n\n"
                    f"User Question:\n{question}"
                )
            }
        ],
        temperature=0.2,
        max_completion_tokens=1000
    )

    return completion.choices[0].message.content
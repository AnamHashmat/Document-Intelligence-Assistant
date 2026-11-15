from services.database import supabase
from services.embedding import get_embedding


def retrieve_documents(
    question,
    match_count=5,
    match_threshold=0.30,
    document_id=None
):
    # Generate embedding for the user's question
    query_embedding = get_embedding(
        question,
        task_type="RETRIEVAL_QUERY"
    )

    # Search Supabase for similar document chunks
    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_threshold": match_threshold,
            "match_count": match_count,
            "filter_document_id": document_id
        }
    ).execute()

    return response.data
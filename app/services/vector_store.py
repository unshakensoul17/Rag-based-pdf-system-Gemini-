from app.core.database import supabase
from typing import List, Dict, Any

class VectorStore:
    @staticmethod
    def store_document(filename: str, upload_hash: str, metadata: Dict[str, Any] = None) -> str:
        """
        Creates a document record in the 'documents' table.
        Returns the document ID.
        """
        data = {
            "filename": filename,
            "upload_hash": upload_hash,
            "metadata": metadata or {}
        }
        response = supabase.table("documents").insert(data).execute()
        return response.data[0]['id']

    @staticmethod
    def store_chunks(document_id: str, chunks: List[Dict[str, Any]]):
        """
        Stores multiple chunks in the 'document_chunks' table.
        chunks: List of dicts containing 'content', 'embedding', 'chunk_index', 'metadata'
        """
        # Add document_id to each chunk
        for chunk in chunks:
            chunk['document_id'] = document_id
            
        # Supabase generic insert
        response = supabase.table("document_chunks").insert(chunks).execute()
        return response.data

    @staticmethod
    def search_similar(embedding: List[float], limit: int = 5, threshold: float = 0.3, filter: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Performs vector similarity search via the 'match_documents' RPC function.
        """
        params = {
            "query_embedding": embedding,
            "match_threshold": threshold,
            "match_count": limit,
            "filter_document_id": filter.get("document_id") if filter else None
        }
        response = supabase.rpc("match_documents", params).execute()
        return response.data

    @staticmethod
    def check_duplicate(upload_hash: str) -> str:
        """
        Checks if a document with the same hash already exists.
        Returns the document ID if found, else None.
        """
        response = supabase.table("documents").select("id").eq("upload_hash", upload_hash).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]['id']
        return None

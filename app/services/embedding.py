import google.generativeai as genai
from app.core.config import settings
from typing import List

genai.configure(api_key=settings.GEMINI_API_KEY)

class EmbeddingService:
    @staticmethod
    def get_embedding(text: str) -> List[float]:
        """
        Generates embedding for a single text string using Gemini API.
        """
        try:
            result = genai.embed_content(
                model=settings.EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise e

    @staticmethod
    def get_query_embedding(text: str) -> List[float]:
        """
        Generates embedding for a query string.
        """
        try:
            result = genai.embed_content(
                model=settings.EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            raise e

    @staticmethod
    def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts (batch processing).
        """
        # Note: Gemini API might have limits on batch size, handled basic list here.
        # For very large lists, we might need to chunk this further.
        if not texts:
            return []
            
        try:
            # Currently embed_content doesn't strictly support list for 'content' in all SDK versions efficiently 
            # as a single batch call with same efficiency as OpenAI's batch.
            # However, we can iterate. For high performance, we might want to check if 
            # batch_embed_contents is available or valid for this model.
            # Assuming simple iteration for now to ensure reliability.
            embeddings = []
            for text in texts:
                embeddings.append(EmbeddingService.get_embedding(text))
            return embeddings
        except Exception as e:
            print(f"Error generating batch embeddings: {e}")
            raise e

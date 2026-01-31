import hashlib
import io
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStore

class IngestionService:
    @staticmethod
    async def process_pdf(file: UploadFile) -> str:
        """
        Reads a PDF file, extracts text, chunks it, generates embeddings, 
        and stores everything in Supabase.
        Returns the Document ID.
        """
        # 1. Read file content
        content = await file.read()
        
        # 2. Generate Hash to check for duplicates
        file_hash = hashlib.sha256(content).hexdigest()
        if VectorStore.check_duplicate(file_hash):
             # Depending on requirements, we could return existing ID or error.
             # For now, let's just return a specific message or handle it.
             # But here assuming we just want to re-process or return existing check is expensive? 
             # Let's simple Check duplicate returns bool.
             # Ideally we should get the ID if it exists. 
             # For simplicity, if duplicate, we raise an exception or handling logic.
             # Let's raise an exception for now to inform user.
             raise HTTPException(status_code=409, detail="Document already exists.")

        # 3. Extract Text
        try:
            pdf_reader = PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")

        if not text.strip():
             raise HTTPException(status_code=400, detail="PDF contains no extractable text.")

        # 4. Create Document Record
        doc_id = VectorStore.store_document(
            filename=file.filename,
            upload_hash=file_hash,
            metadata={"size": len(content), "type": "pdf"}
        )

        # 5. Chunk Text
        chunks = ChunkingService.chunk_text(text)
        
        # 6. Generate Embeddings & Prepare for Storage
        # We can do this in batches if needed. 
        # For simplicity, we process all at once, but for large PDFs, batching is better.
        chunks_data = []
        
        # Batch size for embedding to avoid hitting API limits too hard
        BATCH_SIZE = 10
        total_chunks = len(chunks)
        
        for i in range(0, total_chunks, BATCH_SIZE):
            batch_texts = chunks[i : i + BATCH_SIZE]
            try:
                batch_embeddings = EmbeddingService.get_batch_embeddings(batch_texts)
                
                for j, (chunk_text, embedding) in enumerate(zip(batch_texts, batch_embeddings)):
                    chunks_data.append({
                        "content": chunk_text,
                        "embedding": embedding,
                        "chunk_index": i + j,
                        "metadata": {}
                    })
            except Exception as e:
                # Log error, maybe cleanup document?
                print(f"Error processing batch {i}: {e}")
                # Use what we have or fail? Fail for data integrity.
                raise HTTPException(status_code=500, detail="Failed to generate embeddings.")

        # 7. Store Chunks
        if chunks_data:
            VectorStore.store_chunks(doc_id, chunks_data)
            
        return doc_id

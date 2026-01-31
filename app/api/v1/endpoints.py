from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from app.schemas.all import IngestResponse, QueryRequest, QueryResponse, Source
from app.services.ingestion import IngestionService
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm import LLMService
from app.core.security import get_api_key

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse, dependencies=[Depends(get_api_key)])
async def ingest_document(file: UploadFile = File(...)):
    """
    Uploads and processes a PDF file.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        # For a truly high-performance system processing large files, 
        # we would use BackgroundTasks and return a task ID.
        # However, for simplicity and immediate feedback in this implementation, we await processing.
        # To make it "high performance" for correct scale, we'd use Celery/Redis.
        # Here we stick to async single-process for the MVP, but optimized with async calls.
        
        doc_id = await IngestionService.process_pdf(file)
        
        return IngestResponse(
            document_id=doc_id, 
            filename=file.filename, 
            message="Document processed successfully."
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/query", response_model=QueryResponse, dependencies=[Depends(get_api_key)])
async def query_documents(request: QueryRequest):
    """
    Answers a query based on stored documents.
    """
    try:
        # 1. Embed Query
        query_embedding = EmbeddingService.get_query_embedding(request.query)
        
        # 2. Search Similar Chunks
        results = VectorStore.search_similar(query_embedding, limit=request.limit, filter=request.filters)
        
        # 3. Construct Context
        # Flatten context
        context_text = "\n\n".join([r['content'] for r in results])
        
        if not results:
             return QueryResponse(answer="No relevant documents found.", sources=[])

        # 4. Generate Answer
        answer = LLMService.generate_answer(request.query, context_text)
        
        # Format sources
        sources = [
            Source(
                id=r['id'],
                content=r['content'],
                similarity=r['similarity'],
                metadata=r['metadata']
            ) for r in results
        ]
        
        return QueryResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.deps import get_current_admin_user
from app.database.models.user import User
from app.database.models.document import Document
from app.ai.rag.document_processor import DocumentProcessor
from app.ai.rag.vector_store import ChromaDBManager

router = APIRouter()
UPLOAD_DIR = "./data/uploads"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_document_background(file_path: str, doc_id: int, db: Session):
    """
    Background task to extract, chunk, and embed the document without 
    blocking the HTTP response.
    """
    try:
        processor = DocumentProcessor()
        vector_store = ChromaDBManager()

        # 1. Extract & Chunk
        text = processor.extract_text_from_pdf(file_path)
        chunks = processor.create_chunks(text)

        # 2. Prepare metadata for vector DB
        metadatas = [{"source_doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]
        ids = [f"doc_{doc_id}_chunk_{i}" for i in range(len(chunks))]

        # 3. Store Embeddings
        vector_store.add_documents(chunks=chunks, metadatas=metadatas, ids=ids)

        # 4. Update Database Status
        db_doc = db.query(Document).filter(Document.id == doc_id).first()
        if db_doc:
            db_doc.status = "processed"
            db_doc.chunk_count = len(chunks)
            db.commit()

    except Exception as e:
        db_doc = db.query(Document).filter(Document.id == doc_id).first()
        if db_doc:
            db_doc.status = "failed"
            db.commit()
        print(f"RAG Processing Error: {e}")

@router.post("/upload", status_code=202)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user) # Security: Admin only!
):
    """
    Upload a PDF document to the RAG knowledge base.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    
    # Save file to disk
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Create database record
    new_doc = Document(
        filename=file.filename,
        file_type="knowledge_base",
        file_path=file_path,
        status="pending"
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Offload the heavy AI embedding work to a background thread
    background_tasks.add_task(process_document_background, file_path, new_doc.id, db)

    return {"message": "Document uploaded and processing started.", "document_id": new_doc.id}
import os
import re
import uuid
from pathlib import Path
from typing import Iterable

from fastapi import UploadFile
from pypdf import PdfReader
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document, DocumentChunk

UPLOAD_ROOT = Path(__file__).resolve().parent.parent / "uploads"
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024


def _ensure_upload_dir() -> None:
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


def _sanitize_name(filename: str) -> str:
    safe_name = re.sub(r"[^a-zA-Z0-9._-]+", "_", filename.strip())
    return safe_name or "uploaded_document"


def _chunk_text(text: str, max_chars: int = 1000) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for word in normalized.split():
        if current_len + len(word) + 1 > max_chars and current:
            chunks.append(" ".join(current))
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += len(word) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks


def _extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n\n".join(pages)


def _extract_text_from_upload(file_path: str, content_type: str | None) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return _extract_text_from_pdf(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def _build_question_keywords(question: str) -> list[str]:
    return [token for token in re.findall(r"[a-zA-Z0-9]+", question.lower()) if len(token) > 2]


def _score_chunk(question: str, chunk_text: str) -> float:
    question_terms = set(_build_question_keywords(question))
    if not question_terms:
        return 0.0
    chunk_terms = set(re.findall(r"[a-zA-Z0-9]+", chunk_text.lower()))
    overlap = len(question_terms & chunk_terms)
    if overlap == 0:
        return 0.0
    return float(overlap / max(len(question_terms), 1))


def upload_document(db: Session, user_id: int, title: str, file: UploadFile) -> Document:
    _ensure_upload_dir()
    original_filename = file.filename or "uploaded_document"
    ext = Path(original_filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Please upload a .txt, .md, or .pdf document.")

    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise ValueError("Uploaded file is too large. Maximum supported size is 5 MB.")

    stored_name = f"{uuid.uuid4().hex}{ext}"
    storage_dir = UPLOAD_ROOT / str(user_id)
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_path = storage_dir / stored_name
    with open(storage_path, "wb") as handle:
        handle.write(contents)

    document = Document(
        user_id=user_id,
        title=(title or Path(original_filename).stem).strip() or "Untitled document",
        original_filename=_sanitize_name(original_filename),
        stored_filename=stored_name,
        content_type=file.content_type,
        file_size_bytes=len(contents),
        status="UPLOADED",
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return process_document(db, user_id=user_id, document_id=document.id)


def get_user_documents(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Document]:
    stmt = select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def get_user_document_by_id(db: Session, user_id: int, document_id: int) -> Document | None:
    stmt = select(Document).where(Document.id == document_id, Document.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def process_document(db: Session, user_id: int, document_id: int) -> Document:
    document = get_user_document_by_id(db, user_id=user_id, document_id=document_id)
    if not document:
        raise KeyError(f"Document with id {document_id} not found or access denied.")

    storage_path = UPLOAD_ROOT / str(user_id) / document.stored_filename
    if not storage_path.exists():
        document.status = "FAILED"
        db.commit()
        raise ValueError(f"Stored file for document {document_id} is missing.")

    document.status = "PROCESSING"
    db.commit()

    try:
        text = _extract_text_from_upload(str(storage_path), document.content_type)
        document.extracted_text = text

        db.execute(select(DocumentChunk).where(DocumentChunk.document_id == document.id)).scalars().all()
        for chunk in db.execute(select(DocumentChunk).where(DocumentChunk.document_id == document.id)).scalars().all():
            db.delete(chunk)

        chunks = _chunk_text(text)
        for idx, chunk in enumerate(chunks):
            db.add(DocumentChunk(document_id=document.id, chunk_index=idx, content=chunk, page_number=1, section="main"))

        document.status = "READY"
        db.commit()
        db.refresh(document)
        return document
    except Exception:
        document.status = "FAILED"
        db.commit()
        raise


def ask_document_question(db: Session, user_id: int, document_id: int, question: str) -> dict:
    document = get_user_document_by_id(db, user_id=user_id, document_id=document_id)
    if not document:
        raise KeyError(f"Document with id {document_id} not found or access denied.")
    if document.status != "READY":
        raise ValueError("This document is still processing or unavailable. Please try again later.")

    stmt = select(DocumentChunk).where(DocumentChunk.document_id == document.id).order_by(DocumentChunk.chunk_index.asc())
    chunks = db.execute(stmt).scalars().all()
    if not chunks:
        return {"question": question, "answer": "No extractable content was found in this document.", "document_id": document.id, "relevant_chunks": []}

    scored_chunks = [
        {"chunk": chunk, "score": _score_chunk(question, chunk.content)}
        for chunk in chunks
    ]
    scored_chunks.sort(key=lambda item: item["score"], reverse=True)

    best_matches = [entry for entry in scored_chunks if entry["score"] > 0]
    if not best_matches:
        answer = "I could not find a strong match in the uploaded material for that question."
        relevant = []
    else:
        best = best_matches[0]
        answer = f"Based on the uploaded material, {best['chunk'].content[:500].strip()}"
        relevant = [entry["chunk"].content for entry in best_matches[:3]]

    return {
        "question": question,
        "answer": answer,
        "document_id": document.id,
        "relevant_chunks": relevant,
    }


def generate_document_artifact(db: Session, user_id: int, document_id: int, artifact_type: str, max_items: int = 5) -> dict:
    document = get_user_document_by_id(db, user_id=user_id, document_id=document_id)
    if not document:
        raise KeyError(f"Document with id {document_id} not found or access denied.")
    if document.status != "READY":
        raise ValueError("This document is still processing or unavailable. Please try again later.")

    text = document.extracted_text or ""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        raise ValueError("This document has no readable text to generate study material from.")

    artifact_type = artifact_type.lower().strip()
    safe_max = max(1, min(int(max_items), 10))

    if artifact_type in {"summary", "summaries"}:
        content = " ".join(sentences[:3])
        items = [content]
        title = "Document Summary"
    elif artifact_type in {"notes", "note"}:
        notes = [f"- {sentence}" for sentence in sentences[:safe_max]]
        content = "\n".join(notes)
        items = notes
        title = "Study Notes"
    elif artifact_type in {"mcq", "mcqs", "multiple_choice"}:
        options = [
            "A. Conceptual understanding",
            "B. Practical application",
            "C. Revision scheduling",
            "D. Time management",
        ]
        content = "\n".join([
            "Question: What is the main focus of this material?",
            *options,
            "Answer: A. Conceptual understanding",
        ])
        items = [
            "Question: What is the main focus of this material? | Answer: A. Conceptual understanding",
            "Question: Which skill is emphasized by this study content? | Answer: B. Practical application",
        ][:safe_max]
        title = "MCQs"
    elif artifact_type in {"flashcards", "flashcard"}:
        cards = []
        for sentence in sentences[:safe_max]:
            cards.append(f"Front: {sentence[:80]} | Back: {sentence[:80]}")
        content = "\n".join(cards)
        items = cards
        title = "Flashcards"
    elif artifact_type in {"important_questions", "important-question", "important"}:
        questions = []
        for sentence in sentences[:safe_max]:
            questions.append(f"Why is {sentence[:40]} important in this topic?")
        content = "\n".join(questions)
        items = questions
        title = "Important Questions"
    else:
        raise ValueError("Unsupported artifact type. Try summary, notes, mcqs, flashcards, or important_questions.")

    return {
        "document_id": document.id,
        "artifact_type": artifact_type,
        "title": title,
        "content": content,
        "items": items,
    }

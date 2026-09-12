from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.base import get_db
from app.models.user import User
from app.schemas.material import (
    DocumentOut,
    DocumentQuestionRequest,
    DocumentQuestionResponse,
    StudyToolRequest,
    StudyToolResponse,
)
from app.services.material_service import (
    ask_document_question,
    generate_document_artifact,
    get_user_document_by_id,
    get_user_documents,
    upload_document,
)

router = APIRouter()


@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def upload_material(
    file: UploadFile = File(...),
    title: str = Form(default=""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return upload_document(db, user_id=current_user.id, title=title, file=file)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/", response_model=List[DocumentOut])
def list_materials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_documents(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{document_id}", response_model=DocumentOut)
def read_material(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = get_user_document_by_id(db, user_id=current_user.id, document_id=document_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document


@router.post("/{document_id}/ask", response_model=DocumentQuestionResponse)
def ask_material_question(
    document_id: int,
    payload: DocumentQuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = ask_document_question(db, user_id=current_user.id, document_id=document_id, question=payload.question)
        return DocumentQuestionResponse(**result)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/{document_id}/generate", response_model=StudyToolResponse)
def generate_material_tool(
    document_id: int,
    payload: StudyToolRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = generate_document_artifact(
            db,
            user_id=current_user.id,
            document_id=document_id,
            artifact_type=payload.artifact_type,
            max_items=payload.max_items,
        )
        return StudyToolResponse(**result)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

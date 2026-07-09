from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import List
from uuid import UUID
import json
from app.schemas.all_schemas import (
    DocumentResponse, SummaryRequest, SummaryResponse, 
    FlashcardListResponse, QuestionListResponse, ChatRequest, 
    ChatResponse, TranslateRequest, TranslateResponse
)
from app.services.document_service import DocumentService
from app.api.dependencies import get_document_service, get_current_user_id
from app.core.config import settings

router = APIRouter(prefix="/documents", tags=["Documentos & IA"])

@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload(file: UploadFile = File(...), user_id: UUID = Depends(get_current_user_id), service: DocumentService = Depends(get_document_service)):
    file.file.seek(0, 2)
    fs = file.file.tell()
    await file.seek(0)
    if fs > settings.MAX_FILE_SIZE_BYTES: raise HTTPException(status_code=413, detail="Arquivo grande.")
    return await service.process_document_upload(file, user_id)

@router.post("/{document_id}/summary", response_model=SummaryResponse)
async def summarize(document_id: UUID, data: SummaryRequest, user_id: UUID = Depends(get_current_user_id), service: DocumentService = Depends(get_document_service)):
    s = await service.get_summary(document_id, user_id, data.level)
    return SummaryResponse(document_id=s.document_id, level=s.level, content=s.content)

@router.get("/{document_id}/flashcards", response_model=FlashcardListResponse)
async def flashcards(document_id: UUID, user_id: UUID = Depends(get_current_user_id), service: DocumentService = Depends(get_document_service)):
    c = await service.get_flashcards(document_id, user_id)
    return {"flashcards": [{"front": i.front, "back": i.back} for i in c]}

@router.get("/{document_id}/questions", response_model=QuestionListResponse)
async def questions(document_id: UUID, user_id: UUID = Depends(get_current_user_id), service: DocumentService = Depends(get_document_service)):
    q = await service.get_questions(document_id, user_id)
    return {"questions": [{"statement": i.statement, "options": json.loads(i.options), "correct_option": i.correct_option} for i in q]}

@router.post("/{document_id}/chat", response_model=ChatResponse)
async def chat(document_id: UUID, data: ChatRequest, user_id: UUID = Depends(get_current_user_id), service: DocumentService = Depends(get_document_service)):
    a = await service.interact_in_chat(document_id, user_id, data.message)
    return ChatResponse(answer=a)

@router.post("/{document_id}/translate", response_model=TranslateResponse)
async def translate(document_id: UUID, data: TranslateRequest, user_id: UUID = Depends(get_current_user_id), service: DocumentService = Depends(get_document_service)):
    r = await service.translate_document_element(document_id, user_id, data.language, data.target_type, data.summary_level)
    return TranslateResponse(translated_text=r)

@router.get("/{document_id}/export")
async def export_data(document_id: UUID, user_id: UUID = Depends(get_current_user_id), service: DocumentService = Depends(get_document_service)):
    c = await service.get_flashcards(document_id, user_id)
    s = await service.get_summary(document_id, user_id, "1_min")
    return {"document_id": str(document_id), "cached_summary_1m": s.content, "flashcards": [{"front": i.front, "back": i.back} for i in c]}
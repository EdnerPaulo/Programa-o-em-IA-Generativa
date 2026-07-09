import os
import uuid
from uuid import UUID
from fastapi import UploadFile, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from app.core.config import settings
from app.models.all_models import Document, Summary, Flashcard, Question, ChatMessage
from app.repositories.specific_repositories import DocumentRepository, SummaryRepository, FlashcardRepository, QuestionRepository, ChatMessageRepository
from app.services.extractor_strategies import TextExtractorFactory
from app.services.llm_service import GeminiLlmService
import json

class DocumentService:
    def __init__(self, doc_repo: DocumentRepository, sum_repo: SummaryRepository, flash_repo: FlashcardRepository, quest_repo: QuestionRepository, chat_repo: ChatMessageRepository, llm: GeminiLlmService):
        self.doc_repo = doc_repo
        self.sum_repo = sum_repo
        self.flash_repo = flash_repo
        self.quest_repo = quest_repo
        self.chat_repo = chat_repo
        self.llm = llm

    async def validate_and_save_file(self, file: UploadFile) -> tuple[str, str]:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        header = await file.read(4)
        await file.seek(0)
        is_pdf = header == b'%PDF'
        is_docx = header == b'PK\x03\x04'
        is_png = header == b'\x89PNG'
        is_jpg = header[:3] == b'\xff\xd8\xff'

        if not (is_pdf or is_docx or is_png or is_jpg):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arquivo inválido.")

        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        storage_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        with open(storage_path, "wb") as buffer:
            while chunk := await file.read(1024 * 64):
                buffer.write(chunk)
        return unique_filename, storage_path

    async def process_document_upload(self, file: UploadFile, user_id: UUID) -> Document:
        filename, storage_path = await self.validate_and_save_file(file)
        file_ext = os.path.splitext(filename)[1]
        try:
            extractor = TextExtractorFactory.get_strategy(file_ext)
            extracted_text = await run_in_threadpool(extractor.extract, storage_path)
        except Exception:
            if os.path.exists(storage_path):
                os.remove(storage_path)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Erro de extração.")
        doc = Document(user_id=user_id, filename=file.filename, storage_path=storage_path, extracted_text=extracted_text)
        return self.doc_repo.add(doc)

    async def get_summary(self, document_id: UUID, user_id: UUID, level: str) -> Summary:
        doc = self.doc_repo.get_user_document(document_id, user_id)
        if not doc: raise HTTPException(status_code=404, detail="Não encontrado.")
        cached = self.sum_repo.get_by_doc_and_level(document_id, level)
        if cached: return cached
        summary_text = await run_in_threadpool(self.llm.generate_summary, doc.extracted_text, level)
        return self.sum_repo.add(Summary(document_id=document_id, level=level, content=summary_text))

    async def get_flashcards(self, document_id: UUID, user_id: UUID) -> list[Flashcard]:
        doc = self.doc_repo.get_user_document(document_id, user_id)
        if not doc: raise HTTPException(status_code=404, detail="Não encontrado.")
        existing = self.flash_repo.get_by_document(document_id)
        if existing: return existing
        cards_data = await run_in_threadpool(self.llm.generate_flashcards, doc.extracted_text)
        return [self.flash_repo.add(Flashcard(document_id=document_id, front=i["front"], back=i["back"])) for i in cards_data]

    async def get_questions(self, document_id: UUID, user_id: UUID) -> list[Question]:
        doc = self.doc_repo.get_user_document(document_id, user_id)
        if not doc: raise HTTPException(status_code=404, detail="Não encontrado.")
        existing = self.quest_repo.get_by_document(document_id)
        if existing: return existing
        q_data = await run_in_threadpool(self.llm.generate_questions, doc.extracted_text)
        return [self.quest_repo.add(Question(document_id=document_id, statement=i["statement"], options=json.dumps(i["options"]), correct_option=i["correct_option"])) for i in q_data]

    async def interact_in_chat(self, document_id: UUID, user_id: UUID, user_message: str) -> str:
        doc = self.doc_repo.get_user_document(document_id, user_id)
        if not doc: raise HTTPException(status_code=404, detail="Não encontrado.")
        history = self.chat_repo.get_history(document_id)
        h_tuples = [(msg.role, msg.content) for msg in history]
        answer = await run_in_threadpool(self.llm.execute_chat_turn, h_tuples, user_message, doc.extracted_text)
        self.chat_repo.add(ChatMessage(document_id=document_id, role="user", content=user_message))
        self.chat_repo.add(ChatMessage(document_id=document_id, role="model", content=answer))
        return answer

    async def translate_document_element(self, document_id: UUID, user_id: UUID, language: str, target_type: str, summary_level: str) -> str:
        doc = self.doc_repo.get_user_document(document_id, user_id)
        if not doc: raise HTTPException(status_code=404, detail="Não encontrado.")
        text = doc.extracted_text if target_type == "text" else (await self.get_summary(document_id, user_id, summary_level)).content
        return await run_in_threadpool(self.llm.translate_content, text, language)
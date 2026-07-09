from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import decode_token
from app.repositories.specific_repositories import UserRepository, DocumentRepository, SummaryRepository, FlashcardRepository, QuestionRepository, ChatMessageRepository
from app.services.auth_service import AuthService
from app.services.document_service import DocumentService
from app.services.llm_service import GeminiLlmService
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_user_repo(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    return AuthService(user_repo)

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    payload = decode_token(token)
    if not payload or payload.get("refresh"):
        raise HTTPException(status_code=401, detail="Token inválido.")
    return UUID(payload.get("sub"))

def get_document_service(session: Session = Depends(get_session)) -> DocumentService:
    return DocumentService(
        doc_repo=DocumentRepository(session), sum_repo=SummaryRepository(session),
        flash_repo=FlashcardRepository(session), quest_repo=QuestionRepository(session),
        chat_repo=ChatMessageRepository(session), llm=GeminiLlmService()
    )
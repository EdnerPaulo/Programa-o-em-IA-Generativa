from uuid import UUID
from typing import Optional, List
from sqlmodel import Session, select
from app.repositories.base_repository import BaseRepository
from app.models.all_models import User, Document, Summary, Flashcard, Question, ChatMessage

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.exec(select(User).where(User.email == email)).first()

class DocumentRepository(BaseRepository[Document]):
    def __init__(self, session: Session):
        super().__init__(session, Document)

    def get_user_document(self, document_id: UUID, user_id: UUID) -> Optional[Document]:
        return self.session.exec(
            select(Document).where(Document.id == document_id, Document.user_id == user_id)
        ).first()

    def list_by_user(self, user_id: UUID) -> List[Document]:
        return list(self.session.exec(select(Document).where(Document.user_id == user_id)).all())

class SummaryRepository(BaseRepository[Summary]):
    def __init__(self, session: Session):
        super().__init__(session, Summary)

    def get_by_doc_and_level(self, document_id: UUID, level: str) -> Optional[Summary]:
        return self.session.exec(
            select(Summary).where(Summary.document_id == document_id, Summary.level == level)
        ).first()

class FlashcardRepository(BaseRepository[Flashcard]):
    def __init__(self, session: Session):
        super().__init__(session, Flashcard)

    def get_by_document(self, document_id: UUID) -> List[Flashcard]:
        return list(self.session.exec(select(Flashcard).where(Flashcard.document_id == document_id)).all())

class QuestionRepository(BaseRepository[Question]):
    def __init__(self, session: Session):
        super().__init__(session, Question)

    def get_by_document(self, document_id: UUID) -> List[Question]:
        return list(self.session.exec(select(Question).where(Question.document_id == document_id)).all())

class ChatMessageRepository(BaseRepository[ChatMessage]):
    def __init__(self, session: Session):
        super().__init__(session, ChatMessage)

    def get_history(self, document_id: UUID, limit: int = 20) -> List[ChatMessage]:
        return list(self.session.exec(
            select(ChatMessage)
            .where(ChatMessage.document_id == document_id)
            .order_by(ChatMessage.created_at.asc())
            .limit(limit)
        ).all())
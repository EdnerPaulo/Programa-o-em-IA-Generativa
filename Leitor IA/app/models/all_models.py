from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    documents: List["Document"] = Relationship(back_populates="user")

class Document(SQLModel, table=True):
    __tablename__ = "documents"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", on_delete="CASCADE")
    filename: str = Field(nullable=False)
    storage_path: str = Field(nullable=False)
    extracted_text: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: User = Relationship(back_populates="documents")
    resumos: List["Summary"] = Relationship(back_populates="document")
    flashcards: List["Flashcard"] = Relationship(back_populates="document")
    questions: List["Question"] = Relationship(back_populates="document")
    chat_history: List["ChatMessage"] = Relationship(back_populates="document")

class Summary(SQLModel, table=True):
    __tablename__ = "summaries"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    document_id: UUID = Field(foreign_key="documents.id", on_delete="CASCADE")
    level: str = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    document: Document = Relationship(back_populates="resumos")

class Flashcard(SQLModel, table=True):
    __tablename__ = "flashcards"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    document_id: UUID = Field(foreign_key="documents.id", on_delete="CASCADE")
    front: str = Field(nullable=False)
    back: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    document: Document = Relationship(back_populates="flashcards")

class Question(SQLModel, table=True):
    __tablename__ = "questions"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    document_id: UUID = Field(foreign_key="documents.id", on_delete="CASCADE")
    statement: str = Field(nullable=False)
    options: str = Field(nullable=False)
    correct_option: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    document: Document = Relationship(back_populates="questions")

class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    document_id: UUID = Field(foreign_key="documents.id", on_delete="CASCADE")
    role: str = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    document: Document = Relationship(back_populates="chat_history")
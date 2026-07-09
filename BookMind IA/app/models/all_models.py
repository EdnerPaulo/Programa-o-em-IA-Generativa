from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)

    user_books: List["UserBook"] = Relationship(back_populates="user")

class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True, nullable=False)
    author: str = Field(nullable=False)
    genre: str = Field(nullable=False)
    description: str = Field(nullable=False)
    is_trending: bool = Field(default=False)  # Indica se está nos "Mais Lidos"

class UserBook(SQLModel, table=True):
    __tablename__ = "user_books"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", on_delete="CASCADE")
    book_id: UUID = Field(foreign_key="books.id", on_delete="CASCADE")
    status: str = Field(default="to_read")  # reading, completed, to_read
    rating: Optional[int] = Field(default=None)
    
    user: User = Relationship(back_populates="user_books")
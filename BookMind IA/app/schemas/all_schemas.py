from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    description: str
    is_trending: Optional[bool] = False

class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    genre: str
    is_trending: bool

class RecommendationResponse(BaseModel):
    recommended_books: List[BookCreate]
    ai_justification: str

class PersonaChatRequest(BaseModel):
    persona_name: str  # ex: Sherlock Holmes, Machado de Assis
    message: str
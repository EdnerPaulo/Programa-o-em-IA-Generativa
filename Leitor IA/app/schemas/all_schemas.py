from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    created_at: datetime

class SummaryRequest(BaseModel):
    level: str = Field(pattern="^(1_min|5_min|complete)$")

class SummaryResponse(BaseModel):
    document_id: UUID
    level: str
    content: str

class FlashcardBase(BaseModel):
    front: str
    back: str

class FlashcardListResponse(BaseModel):
    flashcards: List[FlashcardBase]

class QuestionBase(BaseModel):
    statement: str
    options: List[str]
    correct_option: str

class QuestionListResponse(BaseModel):
    questions: List[QuestionBase]

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

class TranslateRequest(BaseModel):
    language: str
    target_type: str = Field(pattern="^(text|summary)$")
    summary_level: Optional[str] = "1_min"

class TranslateResponse(BaseModel):
    translated_text: str
import os

project_files = {
    "app/core/config.py": """from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/bookmind"
    GEMINI_API_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()""",

    "app/models/all_models.py": """from uuid import UUID, uuid4
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
    
    user: User = Relationship(back_populates="user_books")""",

    "app/schemas/all_schemas.py": """from pydantic import BaseModel, Field
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
    message: str""",

    "app/services/llm_recommendation_service.py": """from google import genai
from google.genai import types
import json
from app.core.config import settings
from app.schemas.all_schemas import BookCreate

class BookRecommendationService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"

    async def generate_recommendations(self, read_books: list, trending_books: list) -> dict:
        \"\"\"Analisa o histórico do usuário e cruza com os mais lidos do mercado\"\"\"
        prompt = (
            f"O usuário já leu os seguintes livros: {json.dumps(read_books)}.\\n"
            f"Os livros mais lidos e em alta no momento são: {json.dumps(trending_books)}.\\n\\n"
            "Com base nisso, recomende 3 livros ideais para ele. Retorne estritamente um JSON no seguinte formato:\\n"
            "{\\n"
            "  'recommended_books': [{ 'title': '...', 'author': '...', 'genre': '...', 'description': '...' }],\\n"
            "  'ai_justification': 'Explicação do porquẽ dessas escolhas baseando-se no perfil do usuário.'\\n"
            "}"
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)

    async def chat_with_persona(self, persona: str, message: str) -> str:
        \"\"\"Simula uma conversa com um autor ou personagem literário\"\"\"
        prompt = (
            f"Você é a seguinte persona literária: {persona}. Responda à mensagem do usuário incorporando perfeitamente "
            f"a personalidade, tom de voz, época e conhecimento dessa persona.\\n\\n"
            f"Usuário: {message}\\n"
            f"{persona}:"
        )
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        return response.text""",

    "app/api/v1/endpoints/recommendations.py": """from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.schemas.all_schemas import RecommendationResponse, PersonaChatRequest
from app.services.llm_recommendation_service import BookRecommendationService
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.all_models import Book, UserBook

router = APIRouter(prefix="/literary", tags=["Inteligência Literária"])

@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(user_id: UUID, session: Session = Depends(get_session)):
    # Busca livros que o usuário já interagiu
    user_history = session.exec(select(Book).join(UserBook).where(UserBook.user_id == user_id)).all()
    history_data = [{"title": b.title, "genre": b.genre} for b in user_history]
    
    # Busca os livros mais lidos/tendências no banco
    trends = session.exec(select(Book).where(Book.is_trending == True)).all()
    trends_data = [{"title": b.title, "author": b.author, "genre": b.genre} for b in trends]
    
    ai_service = BookRecommendationService()
    result = await ai_service.generate_recommendations(history_data, trends_data)
    return result

@router.post("/chat-persona")
async def chat_with_character(data: PersonaChatRequest):
    ai_service = BookRecommendationService()
    reply = await ai_service.chat_with_persona(data.persona_name, data.message)
    return {"persona": data.persona_name, "response": reply}""",

    "app/main.py": """from fastapi import FastAPI
from app.api.v1.endpoints import recommendations
from app.db.session import init_db

app = FastAPI(title="BookMind IA - API Literária", version="1.0.0")

@app.on_event("startup")
def on_startup():
    try:
        init_db()
    except Exception:
        pass # Ignora caso o banco de dados não esteja conectado localmente ainda

app.include_router(recommendations.router, prefix="/api/v1")"""
}

print("📚 Criando estrutura do BookMind IA...")
for filepath, content in project_files.items():
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  [Criado] -> {filepath}")

print("\n✨ Pronto! O esqueleto do seu novo projeto voltado para livros e recomendações está gerado.")
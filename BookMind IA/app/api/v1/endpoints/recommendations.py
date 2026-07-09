from fastapi import APIRouter, Depends, HTTPException
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
    return {"persona": data.persona_name, "response": reply}
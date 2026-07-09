from google import genai
from google.genai import types
import json
from app.core.config import settings
from app.schemas.all_schemas import BookCreate

class BookRecommendationService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"

    async def generate_recommendations(self, read_books: list, trending_books: list) -> dict:
        """Analisa o histórico do usuário e cruza com os mais lidos do mercado"""
        prompt = (
            f"O usuário já leu os seguintes livros: {json.dumps(read_books)}.\n"
            f"Os livros mais lidos e em alta no momento são: {json.dumps(trending_books)}.\n\n"
            "Com base nisso, recomende 3 livros ideais para ele. Retorne estritamente um JSON no seguinte formato:\n"
            "{\n"
            "  'recommended_books': [{ 'title': '...', 'author': '...', 'genre': '...', 'description': '...' }],\n"
            "  'ai_justification': 'Explicação do porquẽ dessas escolhas baseando-se no perfil do usuário.'\n"
            "}"
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)

    async def chat_with_persona(self, persona: str, message: str) -> str:
        """Simula uma conversa com um autor ou personagem literário"""
        prompt = (
            f"Você é a seguinte persona literária: {persona}. Responda à mensagem do usuário incorporando perfeitamente "
            f"a personalidade, tom de voz, época e conhecimento dessa persona.\n\n"
            f"Usuário: {message}\n"
            f"{persona}:"
        )
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        return response.text
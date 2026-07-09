import json
from google import genai
from google.genai import types
from app.core.config import settings

class GeminiLlmService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"

    def generate_summary(self, text: str, level: str) -> str:
        prompts = {
            "1_min": "Forneça um resumo ultra-condensado de no máximo 3 frases legível em 1 minuto.",
            "5_min": "Forneça um resumo detalhado e estruturado em seções principais legível em 5 minutos.",
            "complete": "Forneça um resumo exaustivo do seguinte documento."
        }
        prompt = f"{prompts.get(level)}\n\nDocumento:\n{text}"
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        return response.text

    def generate_flashcards(self, text: str) -> list:
        prompt = f"Gere flashcards em formato JSON válido (array de objetos com chaves 'front' e 'back') baseados no texto:\n{text}"
        response = self.client.models.generate_content(
            model=self.model, contents=prompt, config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)

    def generate_questions(self, text: str) -> list:
        prompt = f"Gere 5 questões de múltipla escolha em JSON válido (chaves 'statement', 'options', 'correct_option') baseadas no texto:\n{text}"
        response = self.client.models.generate_content(
            model=self.model, contents=prompt, config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)

    def translate_content(self, text: str, target_language: str) -> str:
        prompt = f"Traduza o seguinte texto para o idioma '{target_language}':\n\n{text}"
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        return response.text

    def execute_chat_turn(self, history_tuples: list, current_message: str, document_context: str) -> str:
        chat_contents = [f"Contexto do documento:\n{document_context}\n\nInstrução: Responda baseando-se estritamente no contexto."]
        for role, content in history_tuples:
            chat_contents.append(f"{role}: {content}")
        chat_contents.append(f"user: {current_message}")
        response = self.client.models.generate_content(model=self.model, contents="\n".join(chat_contents))
        return response.text
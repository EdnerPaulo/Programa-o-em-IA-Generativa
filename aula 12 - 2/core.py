"""
Lógica de domínio do agente: validação/sanitização de entrada do usuário,
controle do histórico de conversa e orquestração da chamada ao
OpenRouterClient.

Mantida separada da camada de UI (app.py) e da camada de transporte
(client.py) para baixo acoplamento e facilidade de testes.
"""

from __future__ import annotations

from agent.client import ChatResult, OpenRouterClient
from agent.config import Settings

MAX_INPUT_CHARS = 4000

DEFAULT_SYSTEM_PROMPT = (
    "Você é um assistente útil, direto e honesto. Responda em português "
    "do Brasil, salvo se o usuário escrever em outro idioma. Quando não "
    "tiver certeza de algo, diga isso explicitamente em vez de inventar "
    "uma resposta."
)


class InvalidUserInputError(Exception):
    """Entrada do usuário vazia, ou maior que o limite permitido."""


def sanitize_user_input(raw_text: str) -> str:
    """
    Valida e limpa a entrada do usuário antes de enviá-la ao modelo.

    - Remove espaços/quebras de linha nas bordas.
    - Rejeita entrada vazia.
    - Aplica um limite de tamanho para evitar payloads excessivos.
    """
    text = raw_text.strip()

    if not text:
        raise InvalidUserInputError("A mensagem não pode estar vazia.")

    if len(text) > MAX_INPUT_CHARS:
        raise InvalidUserInputError(
            f"A mensagem excede o limite de {MAX_INPUT_CHARS} caracteres."
        )

    return text


class ConversationAgent:
    """
    Encapsula uma conversa com o modelo, incluindo o prompt de sistema
    e o histórico de turnos (limitado para controlar custo/latência).
    """

    def __init__(
        self,
        client: OpenRouterClient,
        settings: Settings,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ):
        self._client = client
        self._settings = settings
        self._system_prompt = system_prompt

    def build_messages(self, history: list[dict], user_text: str) -> list[dict]:
        """
        Monta a lista de mensagens no formato esperado pela API, aplicando
        o prompt de sistema e truncando o histórico ao limite configurado.
        """
        trimmed_history = history[-self._settings.max_history_messages :]
        return (
            [{"role": "system", "content": self._system_prompt}]
            + trimmed_history
            + [{"role": "user", "content": user_text}]
        )

    def ask(
        self,
        history: list[dict],
        raw_user_text: str,
        model: str | None = None,
        temperature: float = 0.7,
    ) -> ChatResult:
        """
        Valida a entrada, monta as mensagens e chama o modelo.
        Propaga InvalidUserInputError e as exceções de OpenRouterClient
        para a camada de UI decidir como exibi-las.
        """
        user_text = sanitize_user_input(raw_user_text)
        messages = self.build_messages(history, user_text)
        return self._client.chat(messages=messages, model=model, temperature=temperature)

"""
Cliente para a API do OpenRouter (compatível com o formato OpenAI
/chat/completions).

Responsável apenas por comunicação HTTP: montar o payload, chamar o
endpoint e traduzir erros de rede/HTTP em exceções de domínio, sem
vazar detalhes internos (stack trace, headers, corpo bruto da resposta)
para a camada de UI.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests

from agent.config import Settings


class OpenRouterError(Exception):
    """Erro genérico de comunicação com a OpenRouter, seguro para exibir ao usuário."""


class OpenRouterAuthError(OpenRouterError):
    """Credenciais inválidas ou ausentes (HTTP 401/403)."""


class OpenRouterRateLimitError(OpenRouterError):
    """Limite de requisições excedido (HTTP 429)."""


@dataclass
class ChatResult:
    content: str
    model: str
    prompt_tokens: int | None
    completion_tokens: int | None


class OpenRouterClient:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._session = requests.Session()

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._settings.openrouter_api_key}",
            "Content-Type": "application/json",
            # Headers recomendados pela OpenRouter para identificar a app.
            "HTTP-Referer": self._settings.app_url,
            "X-Title": self._settings.app_title,
        }

    def chat(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> ChatResult:
        """
        Envia uma lista de mensagens (formato OpenAI: [{"role": ..., "content": ...}])
        e retorna a resposta do modelo.
        """
        payload = {
            "model": model or self._settings.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        url = f"{self._settings.openrouter_base_url}/chat/completions"

        try:
            response = self._session.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=self._settings.request_timeout,
            )
        except requests.Timeout as exc:
            raise OpenRouterError(
                "Tempo limite excedido ao chamar a OpenRouter. Tente novamente."
            ) from exc
        except requests.RequestException as exc:
            raise OpenRouterError(
                "Falha de rede ao chamar a OpenRouter. Verifique sua conexão."
            ) from exc

        if response.status_code in (401, 403):
            raise OpenRouterAuthError(
                "Chave de API inválida ou sem permissão. Verifique "
                "OPENROUTER_API_KEY."
            )
        if response.status_code == 429:
            raise OpenRouterRateLimitError(
                "Limite de requisições do modelo gratuito atingido. "
                "Aguarde um pouco ou troque de modelo."
            )
        if not response.ok:
            # Não repassamos o corpo bruto da resposta para o usuário final.
            raise OpenRouterError(
                f"A OpenRouter retornou um erro (HTTP {response.status_code})."
            )

        try:
            data = response.json()
            choice = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
        except (KeyError, IndexError, ValueError) as exc:
            raise OpenRouterError(
                "Resposta inesperada da OpenRouter (formato inválido)."
            ) from exc

        return ChatResult(
            content=choice,
            model=data.get("model", payload["model"]),
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
        )

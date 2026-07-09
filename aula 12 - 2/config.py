"""
Configuração central do agente.

Nenhum segredo é hardcoded aqui. Todas as credenciais vêm de variáveis
de ambiente (localmente via .env / python-dotenv, em produção via
variáveis de ambiente configuradas no Render).
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Carrega variáveis de um arquivo .env local, se existir.
# Em produção (Render) as variáveis já vêm do ambiente do serviço.
load_dotenv()


class ConfigError(Exception):
    """Erro de configuração ausente ou inválida."""


@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str
    openrouter_base_url: str
    default_model: str
    app_title: str
    app_url: str
    request_timeout: int
    max_history_messages: int


def _get_env(name: str, default: str | None = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise ConfigError(
            f"Variável de ambiente obrigatória '{name}' não foi definida. "
            f"Configure-a no arquivo .env (local) ou nas variáveis de "
            f"ambiente do serviço no Render."
        )
    return value or ""


def load_settings() -> Settings:
    return Settings(
        openrouter_api_key=_get_env("OPENROUTER_API_KEY", required=True),
        openrouter_base_url=_get_env(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        ),
        # openrouter/free é o auto-router gratuito da OpenRouter: ele escolhe
        # automaticamente um modelo :free disponível, o que evita quebrar a
        # aplicação quando um modelo específico sai da lista gratuita.
        default_model=_get_env("OPENROUTER_MODEL", "openrouter/free"),
        app_title=_get_env("APP_TITLE", "Agente Python + OpenRouter"),
        # Usados nos headers HTTP-Referer / X-Title exigidos pela OpenRouter
        # para ranqueamento e identificação da aplicação nos logs deles.
        app_url=_get_env("APP_URL", "https://localhost:8501"),
        request_timeout=int(_get_env("REQUEST_TIMEOUT_SECONDS", "60")),
        max_history_messages=int(_get_env("MAX_HISTORY_MESSAGES", "20")),
    )

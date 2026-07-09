"""
Interface Streamlit do agente.

Responsabilidade única: renderizar a UI e gerenciar o estado de sessão.
Toda a lógica de negócio fica em agent/core.py e agent/client.py.
"""

import streamlit as st

from agent.client import (
    OpenRouterAuthError,
    OpenRouterClient,
    OpenRouterError,
    OpenRouterRateLimitError,
)
from agent.config import ConfigError, load_settings
from agent.core import (
    DEFAULT_SYSTEM_PROMPT,
    ConversationAgent,
    InvalidUserInputError,
)

# Modelos gratuitos sugeridos. O catálogo de modelos :free da OpenRouter
# muda com frequência — "openrouter/free" (auto-router) é o valor mais
# resiliente por padrão. Os demais são exemplos comuns em julho/2026,
# mas sempre confira a disponibilidade atual em openrouter.ai/models.
SUGGESTED_MODELS = [
    "openrouter/free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "openai/gpt-oss-120b:free",
    "openai/gpt-oss-20b:free",
]


def init_page() -> None:
    st.set_page_config(
        page_title="Agente Python + OpenRouter",
        page_icon="🤖",
        layout="centered",
    )


def load_agent_dependencies():
    """
    Carrega settings e monta o client/agent uma única vez por sessão.
    Erros de configuração (ex.: API key ausente) são exibidos de forma
    amigável, sem interromper a aplicação com um traceback cru.
    """
    if "settings" in st.session_state:
        return st.session_state.settings, st.session_state.client

    try:
        settings = load_settings()
    except ConfigError as exc:
        st.error(str(exc))
        st.info(
            "Crie um arquivo `.env` na raiz do projeto com "
            "`OPENROUTER_API_KEY=sua_chave_aqui` (veja `.env.example`)."
        )
        st.stop()

    client = OpenRouterClient(settings)
    st.session_state.settings = settings
    st.session_state.client = client
    return settings, client


def init_session_state(default_model: str) -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []  # histórico exibido e enviado ao modelo
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = default_model
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT


def render_sidebar(settings) -> tuple[str, float]:
    with st.sidebar:
        st.header("⚙️ Configurações")

        model = st.selectbox(
            "Modelo (OpenRouter)",
            options=SUGGESTED_MODELS,
            index=SUGGESTED_MODELS.index(st.session_state.selected_model)
            if st.session_state.selected_model in SUGGESTED_MODELS
            else 0,
        )
        custom_model = st.text_input(
            "Ou informe outro model ID",
            placeholder="ex: qwen/qwen3-coder:free",
        )
        if custom_model.strip():
            model = custom_model.strip()
        st.session_state.selected_model = model

        temperature = st.slider("Temperatura", 0.0, 1.5, 0.7, 0.1)

        with st.expander("Prompt de sistema"):
            st.session_state.system_prompt = st.text_area(
                "Instrução base do agente",
                value=st.session_state.system_prompt,
                height=120,
            )

        st.divider()
        if st.button("🗑️ Limpar conversa", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.caption(f"Endpoint: `{settings.openrouter_base_url}`")

    return model, temperature


def render_history() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main() -> None:
    init_page()
    settings, client = load_agent_dependencies()
    init_session_state(settings.default_model)

    st.title("🤖 Agente Python + OpenRouter")
    st.caption(
        "Chat construído em Streamlit, usando modelos gratuitos da OpenRouter."
    )

    model, temperature = render_sidebar(settings)
    render_history()

    user_text = st.chat_input("Digite sua mensagem...")
    if user_text is None:
        return

    agent = ConversationAgent(
        client=client,
        settings=settings,
        system_prompt=st.session_state.system_prompt,
    )

    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Pensando...")
        try:
            result = agent.ask(
                history=st.session_state.messages,
                raw_user_text=user_text,
                model=model,
                temperature=temperature,
            )
        except InvalidUserInputError as exc:
            placeholder.warning(str(exc))
            return
        except OpenRouterAuthError as exc:
            placeholder.error(str(exc))
            return
        except OpenRouterRateLimitError as exc:
            placeholder.warning(str(exc))
            return
        except OpenRouterError as exc:
            placeholder.error(str(exc))
            return

        placeholder.markdown(result.content)

    # Só persiste no histórico depois de uma resposta bem-sucedida.
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.messages.append(
        {"role": "assistant", "content": result.content}
    )


if __name__ == "__main__":
    main()

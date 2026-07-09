# Agente Python + OpenRouter (Streamlit)

Agente de chat em Python que usa modelos **gratuitos** da [OpenRouter](https://openrouter.ai)
através de uma interface em **Streamlit**, pronto para deploy no **Render** via **GitHub**.

## Arquitetura

```
agente-openrouter/
├── app.py                  # Interface Streamlit (UI e estado de sessão)
├── agent/
│   ├── __init__.py
│   ├── config.py            # Carregamento de variáveis de ambiente / settings
│   ├── client.py            # Cliente HTTP da API da OpenRouter
│   └── core.py               # Validação de entrada + orquestração da conversa
├── .streamlit/
│   └── config.toml          # Tema e configuração do servidor Streamlit
├── requirements.txt
├── render.yaml               # Configuração de deploy no Render (Blueprint)
├── .env.example
├── .gitignore
└── README.md
```

Separação de responsabilidades:
- **`app.py`** — apenas UI.
- **`agent/core.py`** — regras de negócio (validação, histórico, prompt de sistema).
- **`agent/client.py`** — comunicação HTTP com a OpenRouter, isolando erros de rede/API.
- **`agent/config.py`** — única fonte de configuração, lendo de variáveis de ambiente.

## Pré-requisitos

- Python 3.11+
- Conta gratuita na [OpenRouter](https://openrouter.ai) e uma API key em
  [openrouter.ai/keys](https://openrouter.ai/keys) (não exige cartão de crédito)
- Conta no [GitHub](https://github.com)
- Conta no [Render](https://render.com)

## Rodando localmente

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/agente-openrouter.git
cd agente-openrouter

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# edite o .env e cole sua OPENROUTER_API_KEY

# 5. Rode a aplicação
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`.

## Sobre os modelos gratuitos da OpenRouter

- O padrão configurado é `openrouter/free`, o **auto-router** da própria
  OpenRouter: ele seleciona automaticamente um modelo `:free` disponível,
  o que evita quebrar a aplicação quando um modelo específico sai da
  lista gratuita (o catálogo `:free` muda com frequência).
- Você pode trocar o modelo direto na barra lateral da aplicação, ou
  fixar outro via variável `OPENROUTER_MODEL`.
- Modelos gratuitos têm limite de requisições (rate limit) por minuto/dia,
  definido pela OpenRouter. Em caso de erro 429, a aplicação exibe um
  aviso e sugere aguardar ou trocar de modelo.
- Confira o catálogo atualizado em [openrouter.ai/models](https://openrouter.ai/models)
  (filtro de preço "Free").

## Publicando no GitHub

```bash
git init
git add .
git commit -m "Agente Python + Streamlit + OpenRouter"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/agente-openrouter.git
git push -u origin main
```

O `.gitignore` já impede que o arquivo `.env` (com sua chave de API) seja
commitado.

## Deploy no Render

### Opção A — Blueprint automático (`render.yaml`)

1. Faça push do repositório para o GitHub (passo acima).
2. No dashboard do Render, clique em **New > Blueprint**.
3. Selecione o repositório `agente-openrouter`. O Render lerá o `render.yaml`
   automaticamente.
4. Quando solicitado, defina a variável de ambiente secreta `OPENROUTER_API_KEY`
   com sua chave real.
5. Clique em **Apply**. O Render fará o build e o deploy automaticamente.

### Opção B — Web Service manual

1. No dashboard do Render, clique em **New > Web Service**.
2. Conecte seu repositório GitHub.
3. Configure:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Em **Environment**, adicione a variável `OPENROUTER_API_KEY` com sua chave.
5. Clique em **Create Web Service**.

Após o deploy, o Render fornece uma URL pública (`https://SEU_APP.onrender.com`)
para acessar o agente.

## Segurança

- A API key nunca é hardcoded — vem exclusivamente de variáveis de ambiente
  (`.env` local, ou variáveis de ambiente do Render em produção).
- Entradas do usuário passam por validação/sanitização (`agent/core.py`)
  antes de serem enviadas ao modelo, com limite de tamanho.
- Erros de rede/API são capturados e traduzidos em mensagens seguras —
  o corpo bruto de respostas de erro da OpenRouter nunca é exposto ao usuário.
- O histórico de conversa é truncado (`MAX_HISTORY_MESSAGES`) para evitar
  payloads excessivos.

## Licença

Use livremente como base para seus projetos.

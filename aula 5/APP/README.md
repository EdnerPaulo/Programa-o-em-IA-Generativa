# 🎓    

Uma plataforma web interativa que combina Inteligência Artificial Generativa e Aprendizado de Máquina local para traduzir, interpretar e desconstruir códigos de programação de forma simples, didática e 100% em português.

## 🚀 Sobre o Projeto
O **EduCode AI** foi desenvolvido com o propósito de mitigar as primeiras barreiras enfrentadas por iniciantes na área de tecnologia (complexidade sintática, documentações densas e o inglês técnico). 

O diferencial do projeto está na sua **arquitetura de processamento híbrido**:
1. **Camada Local (Análise Estrutural):** O sistema utiliza uma rede neural de processamento de linguagem natural (NLP) baseada em um codificador Sequence-to-Sequence (Seq2Seq) construída sobre o **TensorFlow**, analisando e extraindo métricas de recorrência e densidade de tokens em tempo real.
2. **Camada Generativa (Explicação Pedagógica):** Os dados textuais tratados são disparados de forma assíncrona para o motor do **Google Gemini API**, que se encarrega de realizar o detalhamento linha por linha, traduzir os comandos e formular analogias lúdicas baseadas na realidade do cotidiano brasileiro.

## 🧠 Tecnologias Utilizadas
* **Python** (Linguagem base do ecossistema)
* **Streamlit** (Interface gráfica interativa)
* **TensorFlow-CPU** (Camada de Machine Learning local para processamento sequencial)
* **Google Gemini API Core** (Interpretação pedagógica de alta fidelidade)
* **Plotly Express & Pandas** (Manipulação e renderização visual das métricas estruturais)
* **Engenharia de Prompt / Regex Parser** (Mecanismo de blindagem e isolamento sintático de respostas)

## 💡 Funcionalidades
* **Identificação Automática:** Detecção instantânea da linguagem de programação fornecida.
* **Explicação Linha por Linha:** Desconstrução detalhada em português claro, omitindo jargões complexos.
* **Tradução Integrada:** Conversão explícita de palavras-chave nativas do inglês (ex: `while` = enquanto, `if` = se).
* **Analogias Práticas:** Associação dos fluxos lógicos a situações do dia a dia (ex: fazer café, pegar ônibus).
* **Métricas por Tensores:** Painel analítico exibindo a densidade do vocabulário dinâmico do algoritmo.

## 🔑 Configuração das Credenciais
Para executar a camada generativa, crie uma chave de acesso gratuita no [Google AI Studio](https://aistudio.google.com/) e insira diretamente na barra lateral da aplicação, ou defina como variável de ambiente em seu servidor de hospedagem sob a chave `GEMINI_API_KEY`.

## ▶️ Como Executar Localmente
```bash
# Clone o repositório do projeto
git clone [https://github.com/seu-usuario/educode-ai](https://github.com/seu-usuario/educode-ai)

# Acesse o diretório correspondente
cd educode-ai

# Instale as dependências contidas no manifesto
pip install -r requirements.txt

# Inicialize o servidor do Streamlit
streamlit run app.py
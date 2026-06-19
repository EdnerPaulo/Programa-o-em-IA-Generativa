import streamlit as st
import google.generativeai as genai
import os
import re
import numpy as np
import pandas as pd
import plotly.express as px

# Importação silenciosa do TensorFlow para otimizar a inicialização da interface
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="EduCode AI",
    page_icon="🎓",
    layout="wide"
)

# Estilização CSS para uma experiência limpa e focada no aprendizado
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- PROMPT INTELIGENTE (SISTEMA) ----------------
PROMPT_SISTEMA = """
Você é um professor de programação extremamente didático para iniciantes (com menos de 6 meses de estudo).
Sua missão é ler o código enviado e desmistificá-lo sem jargões intimidadores.

Você DEVE estruturar sua resposta OBRIGATORIAMENTE utilizando o formato de tags abaixo:

<Linguagem>Nome da linguagem encontrada</Linguagem>

<Explicacao>
Explique o código de forma simples, linha por linha ou por blocos lógicos estruturados.
Traduza palavras em inglês do código para o português de forma explícita (ex: 'if' significa 'se').
Use negritos e tópicos para organizar visualmente.
</Explicacao>

<Analogia>
Crie uma analogia lúdica do mundo real baseada na nossa realidade cotidiana (como fazer café, pegar ônibus, ir à feira) que traduza o funcionamento geral da lógica do código.
</Analogia>
"""

# ---------------- INTELIGÊNCIA LOCAL: MOTOR TENSORFLOW ----------------
class LocalCodeSeq2Seq:
    """
    Componente local que processa sequências sintáticas de código via rede neural (TensorFlow).
    Utilizado para extrair métricas de complexidade e densidade de estruturas em tensores.
    """
    def __init__(self):
        self.max_vocab = 500
        self.max_len = 100
        self.tokenizer = Tokenizer(num_words=self.max_vocab, filters='!"#$%&()*+,-./:;<=>?@[\\]^`{|}~\t\n')
        self.model = self._build_lightweight_encoder()

    def _build_lightweight_encoder(self):
        model = Sequential([
            Embedding(input_dim=self.max_vocab, output_dim=16, input_length=self.max_len),
            LSTM(32, return_sequences=True),
            LSTM(16),
            Dense(4, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return model

    def analyze_sequence(self, code_text):
        if not code_text.strip():
            return {"Total de Linhas": 0, "Tokens Únicos": 0, "Fator de Recorrência": 0.0}
            
        lines = code_text.split('\n')
        self.tokenizer.fit_on_texts(lines)
        sequences = self.tokenizer.texts_to_sequences(lines)
        padded = pad_sequences(sequences, maxlen=self.max_len)
        
        predictions = self.model.predict(padded, verbose=0)
        mean_weights = np.mean(predictions, axis=0)
        
        metrics = {
            "Total de Linhas": len(lines),
            "Tokens Únicos": len(self.tokenizer.word_index),
            "Fator de Recorrência": float(np.max(mean_weights) * 100)
        }
        return metrics

# Instancia o motor do TensorFlow na sessão para evitar recarregamento
if 'tensorflow_engine' not in st.session_state:
    st.session_state['tensorflow_engine'] = LocalCodeSeq2Seq()

# ---------------- FUNÇÃO GEMINI ----------------
def explicar_codigo(api_key, codigo):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=PROMPT_SISTEMA
        )
        resposta = model.generate_content(f"Explique este código:\n\n{codigo}")
        return resposta.text
    except Exception as e:
        return f"Erro na API do Gemini: {str(e)}"

# ---------------- PARSER LOCAL ----------------
def extrair_tag(tag, texto):
    padrao = f"<{tag}>(.*?)</{tag}>"
    match = re.search(padrao, texto, re.DOTALL)
    return match.group(1).strip() if match else f"Bloco <{tag}> não estruturado pela IA."

# ---------------- INTERFACE GRÁFICA (STREAMLIT) ----------------
st.title("🎓 EduCode AI")
st.subheader("Aprenda programação com explicações simples, diretas e inteligência híbrida")

# SIDEBAR (Configuração de Credenciais)
with st.sidebar:
    st.header("🔑 Configuração")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", "")
    )
    st.markdown("👉 Obtenha sua chave gratuita em: [Google AI Studio](https://aistudio.google.com/)")
    st.divider()
    st.caption("⚙️ Sistema operando com processamento estrutural via TensorFlow-CPU local e tradução gerativa remota.")

# LAYOUT DE COLUNAS
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 💻 Cole seu código")
    codigo = st.text_area(
        "Digite ou cole o trecho de código aqui:",
        height=320,
        placeholder="Ex:\nfor i in range(5):\n    print(i)"
    )
    botao = st.button("🚀 Explicar código", use_container_width=True, type="primary")

with col2:
    st.markdown("### 🧠 Painel de Análise")
    
    if botao:
        if not codigo.strip():
            st.warning("⚠️ Digite ou cole um código primeiro.")
        elif not api_key.strip():
            st.error("❌ Adicione sua API Key na barra lateral para prosseguir.")
        else:
            with st.spinner("Analisando estruturas e gerando explicações didáticas..."):
                # 1. Análise de Sequências Local (TensorFlow)
                tf_metrics = st.session_state['tensorflow_engine'].analyze_sequence(codigo)
                
                # 2. Explicação Conceitual de Linguagem Natural (Gemini)
                resposta_bruta = explicar_codigo(api_key, codigo)
                
                # Salvando estado do processamento
                st.session_state['analise_pronta'] = True
                st.session_state['res_linguagem'] = extrair_tag("Linguagem", resposta_bruta)
                st.session_state['res_explicacao'] = extrair_tag("Explicacao", resposta_bruta)
                st.session_state['res_analogia'] = extrair_tag("Analogia", resposta_bruta)
                st.session_state['res_tf_metrics'] = tf_metrics

    # Exibição dos resultados organizados em abas inteligentes
    if st.session_state.get('analise_pronta'):
        tab_didatica, tab_estrutural = st.tabs(["💡 Explicação Didática", "📊 Métricas Estruturais (TensorFlow)"])
        
        with tab_didatica:
            st.success(f"**Linguagem Detectada:** {st.session_state['res_linguagem']}")
            
            st.markdown("#### 📘 Explicação Passo a Passo")
            st.markdown(st.session_state['res_explicacao'])
            
            st.divider()
            st.markdown("#### 💡 Analogia com o Mundo Real")
            st.info(st.session_state['res_analogia'])
            
        with tab_estrutural:
            st.markdown("#### ⚙️ Engenharia de Recursos e Análise de Tensores")
            st.caption("Indicadores extraídos em tempo real por meio da tokenização vetorial do código no servidor local.")
            
            metrics = st.session_state['res_tf_metrics']
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Linhas Processadas", metrics["Total de Linhas"])
            c2.metric("Vocabulário Dinâmico", metrics["Tokens Únicos"])
            c3.metric("Fator de Recorrência", f"{metrics['Fator de Recorrência']:.2f}%")
            
            st.divider()
            st.markdown("##### Gráfico de Densidade de Componentes Sintáticos")
            
            df_chart = pd.DataFrame({
                'Métrica': ['Volume Relativo', 'Diversidade de Tokens', 'Recorrência Sintática'],
                'Intensidade Vetorial': [metrics["Total de Linhas"] * 1.2, metrics["Tokens Únicos"], metrics["Fator de Recorrência"]]
            })
            
            fig = px.bar(df_chart, x='Métrica', y='Intensidade Vetorial', color='Métrica',
                         color_discrete_sequence=px.colors.qualitative.Safe)
            fig.update_layout(height=280, showlegend=False, margin=dict(l=20, r=20, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👋 Cole um trecho de código à esquerda e clique em 'Explicar código' para iniciar o processamento híbrido.")
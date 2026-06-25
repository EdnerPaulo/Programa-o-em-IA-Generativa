import streamlit as st
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from deep_translator import GoogleTranslator
from collections import Counter

# --- Configurações Iniciais e Downloads ---
st.set_page_config(page_title="Análise de Sentimento & NLP", layout="wide")

@st.cache_resource
def load_nlp_resources():
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    try:
        nlp = spacy.load("pt_core_news_sm")
    except OSError:
        from spacy.cli import download
        download("pt_core_news_sm")
        nlp = spacy.load("pt_core_news_sm")
    return nlp, stopwords.words('portuguese'), SentimentIntensityAnalyzer()

nlp, stop_words, sia = load_nlp_resources()

# --- Interface do Usuário (Streamlit) ---
st.title("🧠 Inteligência de Dados: Análise de Feedback de Clientes")
st.markdown("Insira o texto bruto abaixo para extrair insights, sentimentos e padrões de comportamento.")

texto_usuario = st.text_area("Texto de Avaliação do Cliente:", height=150, 
                             placeholder="Digite ou cole a avaliação aqui...")

if st.button("Executar Análise Crítica", type="primary"):
    if not texto_usuario.strip():
        st.warning("Por favor, insira algum texto para iniciar a análise.")
    else:
        # =====================================================================
        # ETAPA 1: Normalização e Limpeza (NLTK & Python)
        # =====================================================================
        texto_minusculo = texto_usuario.lower()
        # Remoção de pontuação
        texto_sem_pontuacao = texto_minusculo.translate(str.maketrans('', '', string.punctuation))
        # Tokenização simples e filtragem de Stop Words
        tokens = texto_sem_pontuacao.split()
        tokens_limpos = [word for word in tokens if word not in stop_words]
        texto_limpo_pt = " ".join(tokens_limpos)

        # =====================================================================
        # ETAPA 2: Análise Morfológica (SpaCy)
        # =====================================================================
        doc = nlp(texto_limpo_pt)
        # Mantendo apenas palavras que não sejam pontuação/espaço (garantia extra)
        tokens_finais = [token.text for token in doc if not token.is_punct and not token.is_space]

        # =====================================================================
        # ETAPA 3: Tradução e Sentimento (Deep-Translator & VADER)
        # =====================================================================
        try:
            # Traduz o texto limpo para o inglês para melhor acurácia no VADER
            texto_en = GoogleTranslator(source='pt', target='en').translate(texto_limpo_pt)
            score_vader = sia.polarity_scores(texto_en)
            compound = score_vader['compound']
        except Exception:
            # Fallback caso ocorra erro na API de tradução
            score_vader = sia.polarity_scores(texto_limpo_pt)
            compound = score_vader['compound']

        # Classificação do sentimento baseado no Compound score
        if compound >= 0.05:
            sentimento = "Positivo"
            cor_metrica = "normal" 
        elif compound <= -0.05:
            sentimento = "Negativo"
            cor_metrica = "inverse"
        else:
            sentimento = "Neutro"
            cor_metrica = "off"

        # =====================================================================
        # ETAPA 4: Contagem e Ordenação
        # =====================================================================
        frequencia = Counter(tokens_finais)
        
        # Converte para DataFrame para ordenação rigorosa (Frequência DESC, Palavra ASC)
        df_freq = pd.DataFrame(frequencia.items(), columns=['Palavra', 'Frequência'])
        df_freq = df_freq.sort_values(by=['Frequência', 'Palavra'], ascending=[False, True]).reset_index(drop=True)

        # =====================================================================
        # EXIBIÇÃO DOS RESULTADOS (Layout Streamlit)
        # =====================================================================
        st.write("---")
        
        # 1. Métricas de Sentimento
        st.subheader("📊 Métricas de Sentimento")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Classificação do Sentimento", value=sentimento, delta=None)
        with col2:
            st.metric(label="Score Compound (VADER)", value=f"{compound:.4f}")

        # 2. Top 5 Termos (Destaque Visual)
        st.subheader("🔥 Top 5 Termos Mais Frequentes")
        top_5 = df_freq.head(5)
        cols_top = st.columns(len(top_5) if len(top_5) > 0 else 1)
        
        if top_5.empty:
            st.info("Nenhum termo relevante encontrado após a filtragem.")
        else:
            for idx, row in top_5.iterrows():
                with cols_top[idx]:
                    st.info(f"**{row['Palavra']}**\n\nRepetições: `{row['Frequência']}`")

        # Layout em duas colunas para a Tabela e a Análise Crítica
        col_tabela, col_analise = st.columns([1, 1])

        with col_tabela:
            # 3. Tabela de Frequência completo
            st.subheader("📋 Tabela Geral de Frequência")
            st.dataframe(df_freq, use_container_width=True, height=300)

        with col_analise:
            # 4. Resumo de Temas (Análise Crítica Automática)
            st.subheader("📝 Resumo de Temas (Análise Crítica)")
            
            termos_chave = ", ".join(top_5['Palavra'].tolist())
            
            if sentimento == "Positivo":
                analise_gerada = (
                    f"A avaliação analisada apresenta uma tonalidade predominantemente **{sentimento}** "
                    f"(Score: {compound:.2f}), indicando satisfação ou engajamento favorável do cliente. "
                    f"Os temas centrais orbitam em torno de palavras-chave como **{termos_chave}**. "
                    "Essa combinação sugere que os pontos fortes do produto, serviço ou experiência "
                    "foram o foco principal do feedback, validando as estratégias operacionais atuais."
                )
            elif sentimento == "Negativo":
                analise_gerada = (
                    f"O motor de NLP identificou uma polaridade **{sentimento}** acentuada "
                    f"(Score: {compound:.2f}). O reuso frequente de termos como **{termos_chave}** "
                    "aponta para gargalos específicos ou fricções na jornada do usuário. Recomenda-se "
                    "uma auditoria imediata sobre os processos ligados a essas palavras para mitigar "
                    "detrações e aplicar ações corretivas."
                )
            else:
                analise_gerada = (
                    f"A análise resultou em uma classificação **{sentimento}** (Score: {compound:.2f}), "
                    "caracterizada por descrições puramente informativas, técnicas ou com equilíbrio entre "
                    f"críticas e elogios. Os termos recorrentes **{termos_chave}** definem o escopo do assunto, "
                    "servindo como um mapa temático do que está sendo discutido, sem viés emocional explícito."
                )
                
            st.markdown(f"> {analise_gerada}")
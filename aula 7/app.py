import streamlit as st # precisa instalar 
import spacy# precisa instalar 
import nltk# precisa instalar 
from nltk.sentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# Instalação rápida caso queira testar: pip install spacy
# Depois baixe o modelo em português: python -m spacy download pt_core_news_sm


# Garante o download do dicionário VADER
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

nlp = spacy.load("pt_core_news_sm")

# Configuração da interface
st.title("Análise de Sentimentos em Português")

# Agora o usuário pode digitar em português
texto_pt = st.text_area("Digite seu texto em português:", "Eu adoro este produto! É maravilhoso.")

if st.button("Analisar Sentimento"):
    fat =   nltk.word_tokenize(texto_pt)
    stops = set(stopwords.words('portuguese'))
    palavras_uteis = [t for t in fat if t.isalnum() and t not in stops]
    documento = nlp(texto_pt)
    
    # Traduz o texto de português (pt) para inglês (en)
    texto_en = GoogleTranslator(source='pt', target='en').translate(texto_pt)
    
    # Inicializa o analisador e calcula os scores no texto traduzido
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(texto_en)
    score_compound = scores['compound']
    
    # Classifica o sentimento com base no score
    if score_compound >= 0.05:
        resultado = "Positivo"
    elif score_compound <= -0.05:
        resultado = "Negativo"
    else:
        resultado = "Neutro"
        

    for token in documento:
        st.success(f"{token.text} -> {token.pos_} ({spacy.explain(token.pos_)})")
   
    st.subheader(f"Resultado: {resultado}")
    st.write(f"**Score Compound:** {score_compound:.4f}")
    st.caption(f"Texto traduzido para análise: *\"{texto_en}\"*")
    st.write(f'TOKENIZAÇÃO - ,  {fat}')
    st.warning(f'STOP WORDS -, {palavras_uteis}')










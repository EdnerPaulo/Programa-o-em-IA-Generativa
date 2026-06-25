import streamlit as st
import pandas as pd
import re
import string
import nltk
import matplotlib.pyplot as plt
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from deep_translator import GoogleTranslator
from wordcloud import WordCloud

# --- Configurações Iniciais da Página ---
st.set_page_config(page_title="Analytics CX & Pipeline PLN", layout="wide")

# --- Inicialização e Cache de Recursos de NLP ---
@st.cache_resource
def carregar_recursos_pln():
    """Baixa recursos do NLTK e carrega o modelo SpaCy com mapeamento didático."""
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    
    try:
        nlp = spacy.load("pt_core_news_sm")
    except OSError:
        from spacy.cli import download
        download("pt_core_news_sm")
        nlp = spacy.load("pt_core_news_sm")
        
    # Dicionário explicativo didático para POS Tags (Siglas -> Nome em PT)
    pos_didatico = {
        "NOUN": "Substantivo (Nomeia objetos, lugares, funções ou ideias)",
        "VERB": "Verbo (Indica ação, estado, processo ou ocorrência)",
        "ADJ": "Adjetivo (Atribui qualidades, defeitos ou características)",
        "ADV": "Advérbio (Modifica o verbo, o adjetivo ou outro advérbio)",
        "PRON": "Pronome (Substitui ou acompanha um substantivo)",
        "DET": "Determinante (Artigos, numerais determinativos)",
        "PROPN": "Nome Próprio (Nome específico de pessoa, lugar ou marca)",
        "ADP": "Preposição (Une termos estabelecendo nexo)",
        "CCONJ": "Conjunção Coordenativa (Conecta orações independentes)",
        "SCONJ": "Conjunção Subordinativa (Conecta orações dependentes)",
        "NUM": "Numeral (Indica quantidade absoluta ou ordem)",
        "AUX": "Verbo Auxiliar (Ajuda a formar tempos compostos)",
        "INTJ": "Interjeição (Exprime emoção súbita)",
        "PUNCT": "Pontuação (Sinais de pontuação)",
        "SYM": "Símbolo (Caracteres especiais, moedas, %)"
    }
    return nlp, stopwords.words('portuguese'), SentimentIntensityAnalyzer(), pos_didatico

nlp, stop_words_pt, sia, pos_explicado = carregar_recursos_pln()

# --- Funções Auxiliares de Exportação ---
@st.cache_data
def converter_para_csv(df):
    """Converte um DataFrame do Pandas em formato CSV legível para download."""
    return df.to_csv(index=False).encode('utf-8')

# --- Interface Gráfica (Streamlit) ---
st.title("🧠 Módulo Avançado de PLN: Inteligência de Atendimento & CX Analytics")
st.markdown("Insira uma mensagem de feedback para visualizar as etapas de engenharia de recursos e roteamento do pipeline.")

# Input de Texto do Usuário
texto_usuario = st.text_area("Mensagem do Cliente (Português):", height=150,
                             placeholder="Exemplo: O aplicativo travou de novo e apresentou um erro crítico no sistema na hora de validar o boleto. Preciso do meu reembolso imediatamente ou vou cancelar o plano.")

if st.button("Processar Pipeline Completo", type="primary"):
    if not texto_usuario.strip():
        st.warning("Por favor, forneça um texto válido para iniciar o processamento do pipeline.")
    else:
        # ==========================================
        # MOTOR DE PROCESSAMENTO (BACKEND DO PIPELINE)
        # ==========================================
        
        # 1. Texto Original
        texto_original = texto_usuario
        
        # 2. Normalização Textual (Minúsculo, sem pontuação, sem números)
        texto_min = texto_original.lower()
        texto_sem_numeros = re.sub(r'\d+', '', texto_min)
        texto_normalizado = texto_sem_numeros.translate(str.maketrans('', '', string.punctuation))
        
        # 3. Tokenização
        tokens_brutos = word_tokenize(texto_normalizado, language='portuguese')
        total_tokens = len(tokens_brutos)
        tokens_unicos = len(set(tokens_brutos))
        
        # 4. Lematização e Análise Morfológica (SpaCy)
        doc = nlp(texto_normalizado)
        dados_lematizacao = []
        dados_pos = []
        lemas_lista = []
        
        for token in doc:
            if token.text.strip():
                # Coleta para Lematização
                dados_lematizacao.append({"Palavra Original": token.text, "Lema (Forma Canônica)": token.lemma_})
                lemas_lista.append(token.lemma_)
                
                # Coleta para POS Tagging
                classe_didatica = pos_explicado.get(token.pos_, "Outros (Estrutura sintática)")
                dados_pos.append({"Palavra": token.text, "Classe Gramatical": token.pos_, "Explicação Didática": classe_didatica})
                
        df_lemas_vinculo = pd.DataFrame(dados_lematizacao)
        df_pos = pd.DataFrame(dados_pos)
        
        # 5. Cálculo de Frequência dos Lemas
        contagem_lemas = Counter(lemas_lista)
        df_freq = pd.DataFrame(contagem_lemas.items(), columns=['Lema', 'Frequência'])
        # Ordenação Decrescente por Frequência, desempate Alfabético por Lema
        df_freq = df_freq.sort_values(by=['Frequência', 'Lema'], ascending=[False, True]).reset_index(drop=True)
        
        # 6. Filtragem de Stopwords (Aplicada sobre a estrutura de lemas)
        stopwords_encontradas = [lema for lema in lemas_lista if lema in stop_words_pt]
        lemas_limpos = [lema for lema in lemas_lista if lema not in stop_words_pt]
        texto_limpo_pt = " ".join(lemas_limpos)
        
        # Contagem pós-filtro para geração do Top 5
        contagem_limpa = Counter(lemas_limpos)
        df_freq_limpa = pd.DataFrame(contagem_limpa.items(), columns=['Lema', 'Frequência'])
        df_freq_limpa = df_freq_limpa.sort_values(by=['Frequência', 'Lema'], ascending=[False, True]).reset_index(drop=True)
        top_5_lemas = df_freq_limpa.head(5)
        
        # 7. Mapeamento de Léxico Negativo
        termos_negativos_alvo = ["erro", "falha", "defeito", "ruim", "péssimo", "bug", "problema", "travou"]
        negativas_detectadas = {termo: lemas_lista.count(termo) for termo in termos_negativos_alvo if lemas_lista.count(termo) > 0}
        
        # 8. Tradução e Sentimento (VADER)
        try:
            texto_en = GoogleTranslator(source='pt', target='en').translate(texto_limpo_pt)
            score_vader = sia.polarity_scores(texto_en)
        except Exception:
            score_vader = sia.polarity_scores(texto_limpo_pt) # Fallback seguro
            
        compound = score_vader['compound']
        
        # Regra híbrida de sentimentos
        if compound <= -0.05 or len(negativas_detectadas) >= 2:
            sentimento_final = "Negativo"
            justificativa_sentimento = f"O texto expressou forte atrito operacional ou insatisfação (Score Compound: {compound:.4f}), corroborado pela presença de léxicos explícitos de falha no idioma de origem."
        elif compound >= 0.05:
            sentimento_final = "Positivo"
            justificativa_sentimento = f"A resposta indica uma estrutura de validação favorável (Score Compound: {compound:.4f}) sem indicadores críticos de quebra de jornada."
        else:
            sentimento_final = "Neutro"
            justificativa_sentimento = f"O texto manteve-se linear (Score Compound: {compound:.4f}), possuindo caráter prioritariamente descritivo ou informativo."

        # 9 e 10. Matriz de Roteamento por Setor
        regras_setoriais = {
            "Suporte Técnico": ["erro", "falha", "bug", "travou", "sistema", "aplicativo"],
            "Financeiro": ["pagamento", "boleto", "fatura", "cobrança", "reembolso"],
            "Cancelamento": ["cancelar", "cancelamento", "encerrar", "desistir"]
        }
        
        palavras_por_setor = {setor: [] for setor in regras_setoriais}
        scores_roteamento = {setor: 0 for setor in regras_setoriais}
        
        for lema in lemas_lista:
            for setor, palavras_chave in regras_setoriais.items():
                if lema in palavras_chave:
                    if lema not in palavras_por_setor[setor]:
                        palavras_por_setor[setor].append(lema)
                    scores_roteamento[setor] += 1
                    
        # Montagem do relatório de roteamento
        dados_roteamento_df = []
        for setor in regras_setoriais:
            termos_achados = ", ".join(palavras_por_setor[setor]) if palavras_por_setor[setor] else "Nenhum"
            dados_roteamento_df.append({"Setor": setor, "Palavras Encontradas": termos_achados, "Score Final": scores_roteamento[setor]})
        df_roteamento = pd.DataFrame(dados_roteamento_df)
        
        # Decisão de Roteamento
        max_score = max(scores_roteamento.values())
        if max_score == 0:
            setor_vencedor = "Atendimento Geral"
        else:
            setor_vencedor = max(scores_roteamento, key=scores_roteamento.get)

        # 11. Reconhecimento de Entidades Nomeadas (NER)
        doc_ner = nlp(texto_original) # NER roda sobre o original para preservar maiúsculas estruturais
        entidades_mapeadas = {"Pessoas": [], "Empresas/Organizações": [], "Locais": [], "Datas": []}
        
        for ent in doc_ner.ents:
            if ent.label_ == "PER":
                entidades_mapeadas["Pessoas"].append(ent.text)
            elif ent.label_ in ["ORG"]:
                entidades_mapeadas["Empresas/Organizações"].append(ent.text)
            elif ent.label_ in ["LOC"]:
                entidades_mapeadas["Locais"].append(ent.text)
            elif ent.label_ in ["MISC", "DATE"]:
                entidades_mapeadas["Datas"].append(ent.text)

        # ==========================================
        # RENDERIZAÇÃO VISUAL DA OUTPUT (EXPECTATION)
        # ==========================================
        st.header("🔬 Relatório Técnico do Pipeline Computacional")
        st.markdown("---")
        
        # 1. Texto Original
        st.subheader("1. Texto Original")
        st.write(texto_original)
        
        # 2. Texto Normalizado
        st.subheader("2. Texto Normalizado")
        st.code(texto_normalizado, language=None)
        
        # 3. Tokenização
        st.subheader("3. Tokenização")
        st.write(tokens_brutos)
        c1, c2 = st.columns(2)
        c1.metric("Quantidade Total de Tokens", total_tokens)
        c2.metric("Quantidade de Palavras Únicas", tokens_unicos)
        
        # 4. Lematização
        st.subheader("4. Lematização")
        st.dataframe(df_lemas_vinculo, use_container_width=True, height=200)
        
        # 5. Frequência dos Lemas
        st.subheader("5. Frequência Geral dos Lemas")
        st.dataframe(df_freq, use_container_width=True)
        
        # 6. Stopwords
        st.subheader("6. Filtragem de Stopwords (NLTK)")
        col_st1, col_st2 = st.columns([1, 2])
        col_st1.metric("Stopwords Removidas", len(stopwords_encontradas))
        col_st1.write("**Termos de ruído encontrados:**")
        col_st1.write(list(set(stopwords_encontradas)))
        with col_st2:
            st.write("**Texto Resultante após Limpeza (Base de Lemas):**")
            st.success(texto_limpo_pt if texto_limpo_pt else "Texto vazio pós-limpeza.")
            
        # 7. Palavras Negativas Encontradas
        st.subheader("7. Palavras Negativas Encontradas")
        if negativas_detectadas:
            df_neg = pd.DataFrame(negativas_detectadas.items(), columns=["Termo Crítico", "Frequência"])
            st.warning("Gatilhados léxicos de insatisfação localizados:")
            st.dataframe(df_neg, use_container_width=True)
        else:
            st.info("Nenhuma palavra de insatisfação crítica foi detectada.")
            
        # 8. Análise Morfológica (POS Tagging)
        st.subheader("8. Análise Morfológica (POS Tagging)")
        st.dataframe(df_pos, use_container_width=True, height=250)
        
        # 9. Análise de Sentimento
        st.subheader("9. Análise Híbrida de Sentimento")
        if sentimento_final == "Positivo":
            st.success(f"Classificação Final: **{sentimento_final}**")
        elif sentimento_final == "Negativo":
            st.error(f"Classificação Final: **{sentimento_final}**")
        else:
            st.warning(f"Classificação Final: **{sentimento_final}**")
        st.write(f"**Score Compound (VADER):** `{compound:.4f}`")
        st.markdown(f"*Justificativa de Engenharia:* {justificativa_sentimento}")
        
        # 10. Palavras-chave por Setor
        st.subheader("10. Palavras-chave Detectadas por Departamento")
        tabs = st.tabs(["Suporte Técnico", "Financeiro", "Cancelamento"])
        for idx, (setor, termos) in enumerate(palavras_por_setor.items()):
            with tabs[idx]:
                if termos:
                    st.write(f"Termos mapeados: {termos}")
                else:
                    st.caption("Nenhuma palavra-chave detectada para este setor.")
                    
        # 11. Score de Roteamento e Decisão
        st.subheader("11. Score de Roteamento e Decisão de Destino")
        st.dataframe(df_roteamento, use_container_width=True)
        st.markdown("#### Direcionamento do Sistema:")
        st.subheader(f"➡️ Destino Final: `{setor_vencedor}`")
        
        # 12 e 13. Gráfico de Frequência e WordCloud
        st.subheader("12 & 13. Elementos Gráficos e Visuais de Distribuição")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.write("**Gráfico de Frequência dos Lemas (Top Itens)**")
            if not df_freq_limpa.empty:
                st.bar_chart(data=df_freq_limpa.head(10), x="Lema", y="Frequência", use_container_width=True)
            else:
                st.caption("Sem dados suficientes.")
                
        with col_g2:
            st.write("**Nuvem de Palavras (Foco em Conteúdo Útil)**")
            if texto_limpo_pt.strip():
                wordcloud = WordCloud(width=600, height=350, background_color="white", max_words=20).generate(texto_limpo_pt)
                fig, ax = plt.subplots(figsize=(6, 3.5))
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.caption("Nuvem indisponível devido ao tamanho do texto limpo.")
                
        # 14. Entidades Nomeadas (NER)
        st.subheader("14. Reconhecimento de Entidades Nomeadas (NER)")
        cont_entidades = 0
        for categ, lista in entidades_mapeadas.items():
            if lista:
                st.markdown(f"**{categ}:** {', '.join(list(set(lista)))}")
                cont_entidades += 1
        if cont_entidades == 0:
            st.info("Nenhuma entidade nomeada mapeada pelo modelo estrutural (PER, ORG, LOC, DATE) foi encontrada.")
            
        # 15. Top 5 Palavras
        st.subheader("15. Top 5 Palavras Mais Frequentes (Pós-Filtro)")
        if not top_5_lemas.empty:
            for rank, r in top_5_lemas.iterrows():
                st.markdown(f"{rank+1}º Lugar: **{r['Lema']}** (Aparece {r['Frequência']}x)")
        else:
            st.caption("Sem dados.")
            
        # 16. Exportação de Dados
        st.subheader("16. Exportação de Relatórios")
        csv_freq = converter_para_csv(df_freq)
        csv_rot = converter_para_csv(df_roteamento)
        
        col_exp1, col_exp2 = st.columns(2)
        col_exp1.download_button(label="📥 Baixar Tabela de Frequência (.csv)", data=csv_freq, file_name="frequencia_lemas.csv", mime="text/csv")
        col_exp2.download_button(label="📥 Baixar Sumário de Roteamento (.csv)", data=csv_rot, file_name="relatorio_roteamento.csv", mime="text/csv")
        
        # 17. Conclusão e Plano de Ação
        st.subheader("17. Conclusão e Plano de Ação")
        lema_principal = top_5_lemas.iloc[0]['Lema'] if not top_5_lemas.empty else "não identificado"
        
        conclusao_texto = (
            f"A análise computacional indica que o feedback do usuário gravita em torno do lema central **'{lema_principal}'**, "
            f"apresentando um padrão de comportamento com sentimento classificado como **{sentimento_final}**. Devido aos acionadores léxicos "
            f"localizados, o motor inteligente enviou automaticamente a demanda para o time de **{setor_vencedor}**. Como plano de ação imediata, "
            f"a equipe operacional deve priorizar este ticket no painel, mitigando as palavras críticas encontradas e gerando uma tratativa humana customizada."
        )
        st.write(conclusao_texto)
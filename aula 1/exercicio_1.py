# Desafio 1: O Cartão de Visitas Digital (Exibição de Texto)
# - **O que fazer:** Crie uma aplicação que sirva como um portfólio simples ou cartão de visitas.
# - **Requisitos:** Você deve usar três funções diferentes de exibição de texto da API do Streamlit: uma para o título principal, outra para subtítulos de seções e uma terceira para blocos de texto comum ou descrições monoespaçadas.
# - **Foco de pesquisa na documentação:** Seção de *Text elements* (`st.title`, `st.header`, `st.text`, `st.markdown`).
import streamlit as st


st.header('Pagina ante-fumantes')
st.title('Venha conhecer o mundo de :rainbow[Malboro]')
st.text ('Fumar é prejudicial a SAUDE')
st.markdown(
    '''
    O :red[Ministerio] da Saude Adverte  &mdash;
    Fumar é BOM  &mdash;\:sunflower:
    Mais MATA com o tempo
'''
)
"""
Componente visual de renderização de gráficos do sistema.
"""
import streamlit as st
import pandas as pd
from typing import List
from models.analise_model import AnaliseModel
from utils.exporter import Exporter

def render_dashboard(analises: List[AnaliseModel]) -> None:
    """Monta métricas e visualizações estruturadas baseadas no histórico."""
    st.markdown("### 📊 Indicadores Gerais")
    
    if not analises:
        st.info("Nenhum dado consolidado disponível para montagem do Dashboard.")
        return

    df = Exporter.para_dataframe(analises)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Capturas", len(df))
    with col2:
        st.metric("Total de Rostos Identificados", int(df["Rostos"].sum()))
    with col3:
        st.metric("Média de Pessoas/Foto", round(df["Pessoas"].mean(), 2))
        
    st.markdown("---")
    
    col4, col5 = st.columns(2)
    with col4:
        st.markdown("**Distribuição de Luminosidade**")
        lum_counts = df["Luminosidade"].value_counts()
        st.bar_chart(lum_counts)
        
    with col5:
        st.markdown("**Qualidade de Foco (Nitidez)**")
        nit_counts = df["Nitidez"].value_counts()
        st.pie_chart(nit_counts)
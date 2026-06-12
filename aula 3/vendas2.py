import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. Cabeçalho do App
st.header("Previsão de Vendas 📈")
st.write("Treinando um modelo de Regressão Linear simples para prever faturamento baseado em marketing.")

# 2. Dados de Treinamento
dados_vendas = pd.DataFrame({
    'investimento': [100, 200, 300, 400, 500, 600],
    'faturamento': [1200, 2500, 3200, 4800, 5100, 6300]
})

# Exibindo os dados na tela de forma organizada
st.subheader("Dados Históricos")
st.dataframe(dados_vendas)

# 3. Treinamento do Modelo de Regressão Linear
# O Scikit-Learn espera que o X (features) seja um DataFrame/matriz 2D e o y (target) seja 1D
X = dados_vendas[['investimento']]
y = dados_vendas['faturamento']

modelo = LinearRegression()
modelo.fit(X, y)

# 4. Interface de Interação com o Usuário
st.subheader("Faça sua Previsão")

# Slider para o usuário escolher o valor do investimento
novo_investimento = st.slider(
    "Escolha o valor do investimento em Marketing (R$):", 
    min_value=0, 
    max_value=1500, 
    value=350, 
    step=50
)

# Realizando a previsão com o valor escolhido
# Passamos como DataFrame para manter o nome da feature idêntico ao do treino
input_usuario = pd.DataFrame({'investimento': [novo_investimento]})
previsao_faturamento = modelo.predict(input_usuario)[0]

# 5. Exibindo o Resultado
st.markdown("---")
st.metric(
    label="Faturamento Previsto", 
    value=f"R$ {previsao_faturamento:,.2f}"
)
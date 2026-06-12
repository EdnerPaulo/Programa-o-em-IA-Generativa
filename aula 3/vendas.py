# import numpy as np 
# from sklearn.tree import DecisionTreeClassifier
# # tempo de uso do produto  X reclamação


# x = np.array([
#     [3,0],
#     [2,0],
#     [3,3],
#     [4,1],
#     [5,1]
# ])

# y = np.array([1,1,1,0,0])

# modelo = DecisionTreeClassifier()
# modelo.fit(x,y)
# print(modelo.predict([[2,10]]))



#investimento de marketing


# import numpy  as np
# from sklearn.linear_model import LinearRegression
# # investimento em mkt 1mil
# X = np.array([[1],[2],[4],[5],[3]])
# # vendas 
# y =  np.array([2,8,4,6,5])



# modelo = LinearRegression()


# modelo.fit(X, y)



# print(modelo.predict([[6]]))


import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.header("Previsão de Vendas")

# Dados: [Investimento em Marketing] -> Faturamento
dados_vendas = pd.DataFrame({
    'investimento': [100, 200, 300, 400, 500, 600],
    'faturamento': [1200, 2500, 3200, 4800, 5100, 6300]
})

# objetivo: previsão de FATURAMENTO baseado nos investimentos
st.subheader("Dados Históricos")
st.dataframe(dados_vendas)

X = dados_vendas[['investimento']]
y = dados_vendas['faturamento']

st.scatter_chart( X , y)
modelo_vendas = LinearRegression()
modelo_vendas.fit(X ,y)

v_vendas = st.slider('investimento',0,12,5)
vendido= modelo_vendas.predict([[v_vendas]])
st.subheader("Faça sua Previsão")
printvendido)
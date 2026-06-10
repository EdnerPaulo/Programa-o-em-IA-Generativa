import streamlit as st
import pandas as pd

st.title("Titulo principal")
if st.button("Clique aqui "):
    st.write("Isso é uma barra ")
    d = pd.read_csv('dados.csv')
    st.bar_chart(d, x = 'mes', y = 'vendas')    

st.write("Isso é um paragrafo ")
# st.map()

dados = {
    'vendas':[100,20,30,60],
    'mês':['jan','fev','mar', 'abril']
}
df = pd.DataFrame(dados)
# df = pd.DataFrame(d)
st.line_chart(df, x = 'mês', y = 'vendas')    


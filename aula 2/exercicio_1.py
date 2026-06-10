import streamlit as st
import numpy as np
# 1. Calculadora Simples

st.title("Calculadora")

numero1 = st.number_input('Primeiro numero')
numero2 = st.number_input('Segundo numero',step=0.1)

if st.button('Resultado'):
    soma= numero1+numero2
    st.success(soma)

# 2. Conversor de Temperatura

st.title("Conversor de Temperatura")

Fahrenheit  = st.number_input('Qual a temperatura em Fahrenheit ')
celcius = 5/9

if st.button('A temperatura em Celsius é'):
    sub=  round((Fahrenheit-32)* celcius,1)
    st.success(sub)

# 3. Calculadora de IMC
st.title("Calculadora IMC")

peso = st.number_input('Qual seu Peso')
altura = st.number_input('Qual sua altura')

if st.button('Resultado do IMC'):
    calculo =  round(peso / (altura ** 2), 2)
    st.success(calculo)

# 4. Gerador de Senhas
st.title("Gerador de Senhas")

if st.button('Senha  Numerica Aleatoria'):
    senha = np.random.randn(1)
    st.success(senha)
    st.write("Este e sua senha aleatoria ")

# 5. Cadastro Simples
st.title(" Cadastro Simples")

pri_nome = st.text_input('Primeiro Nome')
ult_nome = st.text_input('Ultimo Nome')
email = st.text_input('E-mail')
telefone = st.number_input('Seu numero de Telefone')


if st.button('Cadastrar'):
    cadastro = [pri_nome+ult_nome,
                email,
                telefone
    ]
    st.success(cadastro)

# 6. Contador

# 7. Tabuada

# 8. Verificador de Número Par ou Ímpar

# 9. Média de Notas

# 10. Sorteador de Nomes
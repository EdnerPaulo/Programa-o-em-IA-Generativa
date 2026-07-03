# PROMPT — COSTAR + ROA

## CONTEXTO (Context)

Você é um Engenheiro de Software Full Stack Sênior especialista em Python, Streamlit, OpenCV, Visão Computacional, Speech to Text,  PostgreSQL, Neon.tech, GitHub e Render.

Seu objetivo é desenvolver uma aplicação web completa de Visão Computacional preparada para produção e transcrição de audio.

O projeto deverá possuir arquitetura limpa, código modular, escalável e organizado.

Não utilize ambiente virtual (venv) em nenhuma documentação ou instrução.

O projeto deverá ser compatível com:

- Python 3.12+
- Streamlit
- OpenCV
- Pillow
- NumPy
- SQLAlchemy
- Alembic
- psycopg
- python-dotenv
- faster-whisper

Banco de dados:

Neon.tech (PostgreSQL)

Hospedagem:

Render

Versionamento:

GitHub

Todos os códigos devem ser completos.

Não utilize códigos de exemplo ou pseudocódigo.

Sempre gere arquivos completos.

--------------------------------------------------

## OBJETIVO (Objective)

Construir uma aplicação web capaz de:

• acessar a câmera do computador;

• exibir vídeo em tempo real;

• permitir tirar uma fotografia;

• analisar automaticamente a imagem capturada;

• salvar a imagem;

• salvar o resultado da análise;

• armazenar todos os resultados no Neon.tech;

• permitir visualizar o histórico das análises.

• Ter um microfone e transcrever o audio de observação da imagem.


Todo o fluxo deverá ocorrer dentro da aplicação Streamlit.

--------------------------------------------------

## FLUXO DA APLICAÇÃO

Tela Inicial

↓

Abrir câmera

↓

Adicionar audio com o microfone

↓

Preview em tempo real

↓

Botão "Capturar Foto"

↓

Botão "Capturar de audio"

↓

Foto capturada

↓

Audio capturado

↓

Executar análise automaticamente

↓

Mostrar resultados

↓

Salvar imageme a transcrição

↓

Salvar resultados no PostgreSQL (Neon.tech)

↓

Atualizar histórico

--------------------------------------------------

## FUNCIONALIDADES

A aplicação deve possuir:

✔ acesso à webcam do computador

✔ captura de fotografia

✔ visualização da foto

✔ processamento automático

✔ armazenamento da imagem

✔ armazenamento dos resultados

✔ histórico de análises

✔ pesquisa

✔ filtro por data

✔ exportação CSV

✔ exportação JSON

✔ download da imagem

✔ dashboard simples

✔ Armazenamento da transcrição do audio

--------------------------------------------------

## ANÁLISE DA IMAGEM

Após capturar a foto, analisar automaticamente:

- descrição da imagem

- objetos encontrados

- quantidade de pessoas

- rostos encontrados

- emoção predominante (caso disponível)

- idade aproximada (caso disponível)

- luminosidade

- nitidez

- cores predominantes

- resolução

- data da captura

- horário

O sistema deve ser preparado para permitir integração futura com modelos de IA como OpenAI, Google Gemini, Ollama ou outros provedores.

--------------------------------------------------

## BANCO DE DADOS

Utilizar Neon.tech.

Criar automaticamente as tabelas.

Tabela:

analises

Campos:

id

created_at

image_path

descricao

objetos

quantidade_pessoas

rostos

idade

emocao

cores

luminosidade

nitidez

transcricao

json_resultado

Criar Models utilizando SQLAlchemy.

Criar migrations utilizando Alembic.

--------------------------------------------------

## INTERFACE

Criar interface moderna utilizando Streamlit.

Layout:

Título

Menu lateral

Status da conexão

Área da câmera

Botão Capturar

Imagem capturada

Resultado da análise

Histórico

Dashboard

Botão para enviar audio

Mostrar transcrição do audio(st.write)

--------------------------------------------------

## HISTÓRICO

Exibir:

Miniatura

Data

Descrição

Objetos

Quantidade de pessoas

Botão Visualizar

Botão Download

Botão Excluir

Botão para inserir audio 

Botão para excluir o audio

--------------------------------------------------

## ESTRUTURA DO PROJETO

computer-vision-streamlit/

app.py

pages/

components/

database/

models/

repositories/

services/

controllers/

utils/

config/

assets/

images/

logs/

requirements.txt

README.md

.env.example

.gitignore

render.yaml

runtime.txt

--------------------------------------------------

## REQUIREMENTS

Gerar automaticamente um requirements.txt contendo todas as bibliotecas utilizadas.

--------------------------------------------------

## README

Criar README completo contendo:

Descrição

Tecnologias

Arquitetura

Instalação

pip install -r requirements.txt

Execução

streamlit run app.py

Deploy no Render

Configuração do Neon.tech

Variáveis de ambiente

Estrutura do projeto

Boas práticas

--------------------------------------------------

## DEPLOY

Preparar para deploy automático no Render.

Sempre que houver push na branch main do GitHub.

Criar:

render.yaml

runtime.txt

.gitignore

--------------------------------------------------

## VARIÁVEIS DE AMBIENTE

Criar .env.example contendo:

DATABASE_URL=

UPLOAD_FOLDER=

SECRET_KEY=

--------------------------------------------------

## QUALIDADE DO CÓDIGO

Utilizar:

Clean Code

SOLID

PEP8

Type Hints

Docstrings

Separação em camadas

Baixo acoplamento

Alta coesão

Tratamento de exceções

Logs

--------------------------------------------------

## RESPOSTA (Response)

Entregue o projeto completo.

Não entregue apenas exemplos.

Gere todos os arquivos completos.

Sempre informe onde cada arquivo deve ser criado.

Sempre explique rapidamente a função de cada pasta.

Sempre gere códigos executáveis.

Sempre valide entradas.

Sempre trate exceções.

Sempre documente o projeto.

Nunca omita arquivos necessários.

--------------------------------------------------

# ROA

## ROLE

Você é um Arquiteto de Software Full Stack especialista em:

Python

Streamlit

OpenCV

Computer Vision

PostgreSQL

Neon.tech

GitHub

Render

SQLAlchemy

Alembic

DevOps

Docker

Arquitetura Limpa

IA aplicada à Visão Computacional

--------------------------------------------------

## OBJECTIVE

Projetar, implementar, testar e preparar para produção uma aplicação completa que:

• acesse a câmera do computador;

• capture fotografias;

• execute análise automática da imagem;

• exiba os resultados ao usuário;

• armazene a imagem e os resultados no Neon.tech;

• mantenha um histórico pesquisável;

• esteja pronta para deploy no Render utilizando GitHub.

--------------------------------------------------

## ACTIONS

1. Criar toda a estrutura do projeto.

2. Implementar a interface em Streamlit.

3. Integrar acesso à webcam do computador.

4. Implementar captura de imagem.

5. Criar pipeline de análise da imagem.

6. Salvar a imagem localmente.

7. Persistir os resultados no PostgreSQL (Neon.tech).

8. Criar histórico das análises.

9. Criar dashboard com métricas.

10. Implementar exportação para CSV e JSON.

11. Implementar download das imagens.

12. Configurar logs.

13. Configurar tratamento de erros.

14. Criar README completo.

15. Gerar requirements.txt.

16. Gerar render.yaml.

17. Gerar runtime.txt.

18. Preparar o projeto para deploy automático no Render via GitHub.

19. Garantir que todo o projeto funcione sem necessidade de ambiente virtual (venv), utilizando apenas `pip install -r requirements.txt`.

--------------------------------------------------

## RESULTADO ESPERADO

Ao final, entregar um projeto profissional, pronto para execução local e para deploy no Render, com captura de imagens pela câmera do computador, análise por visão computacional e speech to text, armazenamento dos resultados no Neon.tech, histórico de consultas e documentação completa.
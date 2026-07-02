# 👁️ VisionHub Production - Plataforma de Visão Computacional

Sistema corporativo de Visão Computacional de ponta a ponta baseado em camadas arquiteturais limpas. O ecossistema integra captura de imagens por meio de hardware físico via Streamlit, processamento numérico de matrizes de imagem com OpenCV, e salvamento relacional na nuvem através do Neon.tech.

## 🚀 Tecnologias Empregadas

- **Linguagem Base:** Python 3.12+
- **Interface e Distribuição:** Streamlit
- **Motor de Visão:** OpenCV (Headless) & Matrix NumPy
- **Mapeador Relacional (ORM):** SQLAlchemy
- **Banco de Dados:** Neon.tech (PostgreSQL Servless)
- **Hospedagem Cloud:** Render (Plano Gratuito)

## 🏗️ Detalhes da Arquitetura de Software

A aplicação foi rigorosamente projetada sobre os princípios do **SOLID** e **Clean Architecture**:
1. **Model**: Define o esquema rígido relacional de dados.
2. **Repository**: Isola os acessos e transações de banco de dados por meio do padrão *Repository Pattern*.
3. **Service (Pipeline)**: Isola os algoritmos puros e computação matemática do OpenCV das regras de negócio.
4. **Controller**: Funciona como intermediário de dados (*Facade*), recebendo as interações do Streamlit e orquestrando onde salvar e como processar.

---

## 🛠️ Instalação e Execução Local

Como o projeto está explicitamente estruturado para não requerer ambientes virtuais isolados (`venv`), a instalação e execução direta ocorrem de forma enxuta:

1. **Instale as dependências diretamente no ambiente:**
   ```bash
   pip install -r requirements.txt
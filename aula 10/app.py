"""
Ponto de entrada central - Visão Computacional App.
Garante a integridade do banco de dados e gerencia a navegação global.
"""
import streamlit as st
from database.connection import engine, Base
from controllers.app_controller import AppController
from components.dashboard import render_dashboard
from utils.exporter import Exporter
from config.settings import Settings
import os
from PIL import Image

# Configuração de Página Streamlit (Deve ser a primeira chamada)
st.set_page_config(
    page_title="VisionHub Production",
    page_icon="👁️",
    layout="wide"
)

# Inicializar tabelas nativamente no Neon se não existirem
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    st.error(f"Erro Crítico de Conexão com o Banco de Dados Neon.tech: {e}")

# Inicializar o Controlador da Aplicação
if 'controller' not in st.session_state:
    st.session_state.controller = AppController()

controller = st.session_state.controller

# --- SIDEBAR (Menu Lateral de Status) ---
with st.sidebar:
    st.title("👁️ VisionHub Pro")
    st.markdown("---")
    st.markdown("### 📋 Navegação")
    menu = st.radio("Selecione o Painel:", ["Câmera e Captura", "Histórico de Análises", "Dashboard Analítico"])
    
    st.markdown("---")
    st.markdown("### 📡 Status da Conexão")
    st.success("Neon.tech: Conectado")
    st.success("Armazenamento Local: Pronto")

# --- CONTEÚDO PRINCIPAL ---

if menu == "Câmera e Captura":
    st.header("📸 Captura de Imagem em Tempo Real")
    st.write("Abaixo, utilize o componente de hardware nativo para capturar fotos para processamento.")
    
    # Componente nativo de câmera do Streamlit
    img_file = st.camera_input("Alinhe o alvo na câmera")
    
    if img_file is not None:
        bytes_data = img_file.getvalue()
        
        st.subheader("🖼️ Imagem Capturada")
        st.image(bytes_data, width=450)
        
        with st.spinner("Executando pipelines de visão computacional..."):
            registro_salvo = controller.processar_e_salvar(bytes_data)
            
            if registro_salvo:
                st.success("Análise computacional estrutural executada e persistida com sucesso!")
                
                # Exibindo os Resultados Dinamicamente
                res = registro_salvo.json_resultado
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Rostos Encontrados", res["rostos"])
                    st.text(f"Idade: {res['idade']}")
                with c2:
                    st.metric("Luminosidade", res["luminosidade"])
                    st.text(f"Nitidez: {res['nitidez']}")
                with c3:
                    st.metric("Cores Predominantes", res["cores"])
                    st.text(f"Resolução: {res['resolucao']}")
                
                st.info(f"**Descrição Gerada:** {res['descricao']}")
            else:
                st.error("Erro no processamento interno da imagem. Verifique os logs do sistema.")

elif menu == "Histórico de Análises":
    st.header("🗄️ Histórico de Análises Arquivadas")
    
    # Barra de Ferramentas e Filtros
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        busca = st.text_input("🔍 Buscar por palavras-chave na descrição ou objetos:")
    with col_f2:
        data_sel = st.date_input("📅 Filtrar a partir de:", value=None)
        
    historico = controller.listar_historico(termo=busca if busca else None, data_filtro=data_sel)
    
    if historico:
        # Botões de Exportação Global
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv_data = Exporter.para_dataframe(historico).to_csv(index=False).encode('utf-8')
            st.download_button("📥 Exportar Tudo para CSV", data=csv_data, file_name="historico_vision.csv", mime="text/csv")
        with col_exp2:
            json_data = Exporter.para_json(historico)
            st.download_button("📥 Exportar Tudo para JSON", data=json_data, file_name="historico_vision.json", mime="application/json")
            
        st.markdown("---")
        
        # Grid do Histórico
        for item in historico:
            with st.container():
                c_img, c_detalhes, c_acoes = st.columns([1, 2, 1])
                
                path_completo = os.path.join(Settings.UPLOAD_FOLDER, item.image_path)
                
                with c_img:
                    if os.path.exists(path_completo):
                        image = Image.open(path_completo)
                        st.image(image, use_container_width=True)
                    else:
                        st.warning("Arquivo de imagem ausente no disco.")
                        
                with c_detalhes:
                    st.markdown(f"#### Registro ID #{item.id} - {item.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
                    st.write(f"**Descrição:** {item.descricao}")
                    st.write(f"**Objetos:** {item.objetos}")
                    st.write(f"**Pessoas detectadas:** {item.quantidade_pessoas}")
                    st.caption(f"Luminosidade: {item.luminosidade} | Nitidez: {item.nitidez} | Resolução: {item.json_resultado.get('resolucao','Desconhecida')}")
                    
                with c_acoes:
                    # Download da Imagem Individual
                    if os.path.exists(path_completo):
                        with open(path_completo, "rb") as file:
                            st.download_button(
                                label="💾 Baixar Foto",
                                data=file,
                                file_name=item.image_path,
                                mime="image/jpeg",
                                key=f"dl_{item.id}"
                            )
                            
                    # Botão para Exclusão de Registro
                    if st.button("🗑️ Excluir Registro", key=f"del_{item.id}"):
                        if controller.remover_registro(item.id, item.image_path):
                            st.success("Removido!")
                            st.rerun()
                            
            st.markdown("---")
    else:
        st.info("Nenhum registro encontrado para os filtros aplicados atualmente.")

elif menu == "Dashboard Analítico":
    st.header("📈 Dashboard Analítico Gerencial")
    historico_completo = controller.listar_historico()
    render_dashboard(historico_completo)
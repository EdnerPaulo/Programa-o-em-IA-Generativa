import streamlit as st
from PIL import Image, ImageOps
import pandas as pd
from ultralytics import YOLO

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA (Interface do Usuário)
# =====================================================================
st.set_page_config(
    page_title="MVP - Detecção de Objetos YOLOv8",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("👁️ Detector de Objetos Inteligente - MVP")
st.markdown("""
    Bem-vindo ao MVP de Visão Computacional. Esta aplicação utiliza o modelo **YOLOv8** para identificar e localizar múltiplos objetos em imagens em tempo real.
""")

# =====================================================================
# 2. BARRA LATERAL DE CONFIGURAÇÕES (Sidebar)
# =====================================================================
st.sidebar.header("⚙️ Configurações do Modelo")

# Slider para ajustar o threshold de confiança do modelo em tempo real
conf_threshold = st.sidebar.slider(
    label="Nível de Confiança Mínimo",
    min_value=0.10,
    max_value=1.00,
    value=0.25,
    step=0.05,
    help="Define o percentual mínimo de certeza que o modelo deve ter para exibir o objeto."
)

# =====================================================================
# 3. LÓGICA DO MODELO (YOLOv8 com Cache)
# =====================================================================
@st.cache_resource
def load_yolo_model(model_name="yolov8n.pt"):
    """
    Carrega o modelo YOLO e o mantém em cache na memória do servidor.
    O download automático ocorre na primeira execução caso o arquivo não exista.
    """
    return YOLO(model_name)

# Inicializa o modelo (usando a versão 'nano' por ser leve e ideal para MVPs)
with st.spinner("Carregando cérebro do sistema (Modelo YOLOv8)..."):
    model = load_yolo_model()

# =====================================================================
# 4. FUNÇÃO AUXILIAR DE IMAGEM
# =====================================================================
def process_uploaded_image(uploaded_file):
    """Lê o arquivo, corrige a orientação EXIF e converte para RGB."""
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    return img.convert("RGB")

# =====================================================================
# 5. ÁREA PRINCIPAL - INTERAÇÃO E PROCESSAMENTO
# =====================================================================
uploaded_file = st.file_uploader(
    label="Escolha uma imagem para análise", 
    type=["jpg", "jpeg", "png"],
    help="Suporta formatos JPG, JPEG e PNG."
)

if uploaded_file is not None:
    try:
        # Carrega a imagem enviada
        image = process_uploaded_image(uploaded_file)
        
        st.subheader("📸 Imagem Original")
        st.image(image, use_container_width=True)
        
        # Botão para disparar a inferência
        if st.button("🚀 Executar Detecção", type="primary"):
            with st.spinner("Analisando pixels e identificando padrões..."):
                # Executa a predição aplicando o threshold do slider
                results = model.predict(image, conf=conf_threshold)
                result = results[0]  # Pega o resultado da imagem atual
                
                # Gera a imagem anotada (YOLO usa BGR, convertemos para RGB para o Streamlit)
                bgr_array = result.plot()
                rgb_array = bgr_array[..., ::-1]
                annotated_img = Image.fromarray(rgb_array)
                
                # Extrai metadados para construir as tabelas de métricas
                detections = []
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    confidence = float(box.conf[0])
                    
                    detections.append({
                        "Classe": class_name,
                        "Confiança": confidence
                    })
            
            st.success("Análise concluída com sucesso!")
            
            # Divide a tela em duas colunas para o painel de resultados
            col_img, col_metrics = st.columns([2, 1])
            
            with col_img:
                st.subheader("🎯 Objetos Detectados")
                st.image(annotated_img, use_container_width=True, caption="Resultado da inferência YOLOv8")
            
            with col_metrics:
                st.subheader("📊 Resumo da Análise")
                
                if len(detections) > 0:
                    df = pd.DataFrame(detections)
                    
                    # Exibe o total geral
                    st.metric(label="Total de Objetos Encontrados", value=len(df))
                    
                    # Contagem agrupada por classe
                    st.markdown("**Quantidade por Categoria:**")
                    class_counts = df['Classe'].value_counts()
                    st.dataframe(class_counts, use_container_width=True)
                    
                    # Lista detalhada de scores
                    st.markdown("**Detalhes Individuais:**")
                    df['Confiança (%)'] = (df['Confiança'] * 100).round(1).astype(str) + '%'
                    st.dataframe(df[['Classe', 'Confiança (%)']], hide_index=True, use_container_width=True)
                else:
                    st.warning("Nenhum objeto detectado com a confiança atual. Tente reduzir o threshold na barra lateral.")
                    
    except Exception as e:
        st.error(f"Erro ao processar imagem: {str(e)}")
else:
    st.info("☝️ Por favor, faça o upload de uma imagem acima para iniciar o processo.")
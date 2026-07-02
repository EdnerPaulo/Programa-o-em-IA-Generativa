import streamlit as st
import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO

# ---------------------------------------------------------
# Configuração da página e Estilização (Fundo em Degradê)
# ---------------------------------------------------------
st.set_page_config(page_title="Segmentação de Imagens - YOLOv8", layout="wide")

# CSS para o degradê com suas cores: #8FC8EB, #4675C0 e #1935A0
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #8FC8EB 0%, #4675C0 50%, #1935A0 100%);
    color: #FFFFFF;
}

h1, h2, h3, p, span, label {
    color: #FFFFFF !important;
}

.stSlider, .stFileUploader {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------------------------------------------------------
# Cabeçalho da Página
# ---------------------------------------------------------
st.title("🔍 Identificação e Segmentação de Imagens")
st.caption("Faça upload de uma imagem para detectar e segmentar objetos automaticamente.")
st.markdown("---")

# ---------------------------------------------------------
# Carregamento do modelo (cache para não recarregar a cada interação)
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    try:
        return YOLO("yolov8n-seg.pt")
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {e}")
        return None

model = load_model()

# ---------------------------------------------------------
# Upload da imagem e Controles
# ---------------------------------------------------------
uploaded_file = st.file_uploader(
    "Envie uma imagem (JPG, PNG)",
    type=["jpg", "jpeg", "png"]
)

conf_threshold = st.slider("Confiança mínima de detecção", 0.1, 0.9, 0.35, 0.05)

if uploaded_file is not None and model is not None:
    # Leitura da imagem
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagem Original")
        st.image(image, use_container_width=True)

    # ---------------------------------------------------------
    # Inferência
    # ---------------------------------------------------------
    with col2:
        with st.spinner("Processando segmentação..."):
            try:
                results = model.predict(
                    source=img_array,
                    conf=conf_threshold,
                    device="cpu",
                    verbose=False
                )

                result = results[0]
                annotated_img = result.plot()
                annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)

                st.subheader("Imagem Segmentada")
                st.image(annotated_img, use_container_width=True)

                # ---------------------------------------------------------
                # Resumo das detecções
                # ---------------------------------------------------------
                st.subheader("📊 Objetos Detectados")

                if result.boxes is not None and len(result.boxes) > 0:
                    classes = result.boxes.cls.cpu().numpy().astype(int)
                    confs = result.boxes.conf.cpu().numpy()
                    names = model.names

                    # ✅ CORREÇÃO: Construir a lista de forma correta
                    summary = []
                    detected = {}
                    for c, conf in zip(classes, confs):
                        label = names[int(c)]
                        detected.setdefault(label, []).append(conf)

                    for label, confs_list in detected.items():
                        summary.append({
                            "Classe": label,
                            "Quantidade": len(confs_list),
                            "Confiança média": f"{np.mean(confs_list):.2f}"
                        })

                    st.table(summary)
                else:
                    st.warning("Nenhum objeto detectado com o nível de confiança selecionado.")

            except Exception as e:
                st.error(f"Erro durante a inferência: {e}")

else:
    if model is None:
        st.error("❌ Modelo não pôde ser carregado. Verifique sua conexão com a internet.")
    else:
        st.info("Aguardando upload de imagem...")
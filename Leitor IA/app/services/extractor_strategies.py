import abc
import fitz
import docx
import easyocr
import numpy as np
from PIL import Image

class TextExtractionStrategy(abc.ABC):
    @abc.abstractmethod
    def extract(self, file_path: str) -> str:
        pass

class PdfExtractionStrategy(TextExtractionStrategy):
    def extract(self, file_path: str) -> str:
        text_content = []
        with fitz.open(file_path) as doc:
            for page in doc:
                text_content.append(page.get_text())
        extracted = "".join(text_content).strip()
        if not extracted:
            ocr_strategy = OcrExtractionStrategy()
            return ocr_strategy.extract(file_path)
        return extracted

class DocxExtractionStrategy(TextExtractionStrategy):
    def extract(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs]).strip()

class OcrExtractionStrategy(TextExtractionStrategy):
    def __init__(self):
        self.reader = easyocr.Reader(["pt", "en"], gpu=False)

    def extract(self, file_path: str) -> str:
        if file_path.lower().endswith(".pdf"):
            text_content = []
            with fitz.open(file_path) as doc:
                for page in doc:
                    pix = page.get_pixmap()
                    img_bytes = pix.tobytes("png")
                    result = self.reader.readtext(img_bytes, detail=0)
                    text_content.append("\n".join(result))
            return "\n".join(text_content).strip()
        else:
            with Image.open(file_path) as img:
                img_np = np.array(img)
                result = self.reader.readtext(img_np, detail=0)
                return "\n".join(result).strip()

class TextExtractorFactory:
    @staticmethod
    def get_strategy(file_extension: str) -> TextExtractionStrategy:
        ext = file_extension.lower()
        if ext == ".pdf":
            return PdfExtractionStrategy()
        elif ext in [".docx", ".doc"]:
            return DocxExtractionStrategy()
        elif ext in [".png", ".jpg", ".jpeg"]:
            return OcrExtractionStrategy()
        raise ValueError("Formato de arquivo não suportado.")
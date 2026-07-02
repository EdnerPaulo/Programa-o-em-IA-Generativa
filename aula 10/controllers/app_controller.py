"""
Orquestrador central de regras de negócio e persistência de dados.
"""
import os
import uuid
from typing import List, Optional
from datetime import date
from config.settings import Settings
from database.connection import get_db_session
from models.analise_model import AnaliseModel
from repositories.analise_repository import AnaliseRepository
from services.cv_service import CVService
from utils.logger import get_logger

logger = get_logger(__name__)

class AppController:
    def __init__(self):
        self.cv_service = CVService()

    def processar_e_salvar(self, image_bytes: bytes) -> Optional[AnaliseModel]:
        """Coordena o fluxo de análise de imagem, escrita em disco e inserção no Neon.tech."""
        db = get_db_session()
        repository = AnaliseRepository(db)
        try:
            # Executar análise matemática
            resultado = self.cv_service.analisar_imagem(image_bytes)
            
            # Salvar fisicamente a imagem
            filename = f"cap_{uuid.uuid4().hex}.jpg"
            full_path = os.path.join(Settings.UPLOAD_FOLDER, filename)
            
            with open(full_path, "wb") as f:
                f.write(image_bytes)

            # Instanciar e preencher o modelo
            nova_analise = AnaliseModel(
                image_path=filename, # Guardar referência relativa para escalabilidade
                descricao=resultado["descricao"],
                objetos=resultado["objetos"],
                quantidade_pessoas=resultado["quantidade_pessoas"],
                rostos=resultado["rostos"],
                idade=resultado["idade"],
                emocao=resultado["emocao"],
                cores=resultado["cores"],
                luminosidade=resultado["luminosidade"],
                nitidez=resultado["nitidez"],
                json_resultado=resultado
            )
            
            return repository.salvar(nova_analise)
        except Exception as e:
            logger.error(f"Erro no fluxo do controlador central: {str(e)}")
            return None
        finally:
            db.close()

    def listar_historico(self, termo: Optional[str] = None, data_filtro: Optional[date] = None) -> List[AnaliseModel]:
        """Retorna os registros recuperados do banco."""
        db = get_db_session()
        repository = AnaliseRepository(db)
        try:
            return repository.buscar_todos(termo, data_filtro)
        finally:
            db.close()

    def remover_registro(self, analise_id: int, filename: str) -> bool:
        """Remove permanentemente o registro do banco e o arquivo do disco."""
        db = get_db_session()
        repository = AnaliseRepository(db)
        try:
            # Remover arquivo local
            full_path = os.path.join(Settings.UPLOAD_FOLDER, filename)
            if os.path.exists(full_path):
                os.remove(full_path)
            return repository.deletar(analise_id)
        finally:
            db.close()
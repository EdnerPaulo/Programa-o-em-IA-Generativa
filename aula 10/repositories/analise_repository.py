"""
Operações CRUD na tabela de análises.
"""
from sqlalchemy.orm import Session
from models.analise_model import AnaliseModel
from utils.logger import get_logger
from typing import List, Optional
from datetime import date

logger = get_logger(__name__)

class AnaliseRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, analise: AnaliseModel) -> AnaliseModel:
        """Persiste uma nova análise no banco de dados."""
        try:
            self.db.add(analise)
            self.db.commit()
            self.db.refresh(analise)
            logger.info(f"Análise salva com sucesso sob ID: {analise.id}")
            return analise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar análise no banco: {str(e)}")
            raise e

    def buscar_todos(self, termo: Optional[str] = None, data_filtro: Optional[date] = None) -> List[AnaliseModel]:
        """Busca análises aplicando filtros de pesquisa estruturados."""
        try:
            query = self.db.query(AnaliseModel)
            if data_filtro:
                query = query.filter(AnaliseModel.created_at >= data_filtro)
            if termo:
                termo_like = f"%{termo}%"
                query = query.filter(
                    (AnaliseModel.descricao.ilike(termo_like)) | 
                    (AnaliseModel.objetos.ilike(termo_like))
                )
            return query.order_by(AnaliseModel.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Erro ao buscar registros: {str(e)}")
            return []

    def deletar(self, analise_id: int) -> bool:
        """Remove um registro baseado em seu ID."""
        try:
            analise = self.db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if analise:
                self.db.delete(analise)
                self.db.commit()
                logger.info(f"Registro {analise_id} removido do banco.")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar registro {analise_id}: {str(e)}")
            return False
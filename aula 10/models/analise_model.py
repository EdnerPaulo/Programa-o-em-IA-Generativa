"""
Mapeamento da tabela 'analises' utilizando SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from database.connection import Base

class AnaliseModel(Base):
    __tablename__ = 'analises'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    image_path = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    objetos = Column(String, nullable=True)
    quantidade_pessoas = Column(Integer, default=0)
    rostos = Column(Integer, default=0)
    idade = Column(String, nullable=True)
    emocao = Column(String, nullable=True)
    cores = Column(String, nullable=True)
    luminosidade = Column(String, nullable=False)
    nitidez = Column(String, nullable=False)
    json_resultado = Column(JSON, nullable=False)
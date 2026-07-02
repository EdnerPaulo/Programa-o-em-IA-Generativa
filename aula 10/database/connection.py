"""
Gerenciador de conexão com o banco de dados Neon.tech compatível com Connection Pooling.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config.settings import Settings
from utils.logger import get_logger

logger = get_logger(__name__)

Base = declarative_base()

try:
    # Removemos o connect_args com statement_timeout para ser 100% compatível com o -pooler do Neon
    engine = create_engine(
        Settings.DATABASE_URL, 
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.critical(f"Falha ao inicializar o motor do banco de dados: {str(e)}")
    raise e

def get_db_session() -> Session:
    """Cria e retorna uma nova sessão síncrona do banco de dados."""
    session = SessionLocal()
    return session
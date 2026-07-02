"""
Módulo de Configuração Estática da Aplicação.
Centraliza as credenciais de bancos de dados gratuitos e caminhos de upload.
"""
import os

class Settings:
    # Busca da tela do Render que você preencheu. Se não achar, usa o plano B.
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg://neondb_owner:npg_hyE6J1Pfkbjl@ep-hidden-mode-ato01bgo-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )
    
    # Validação do driver necessária para o SQLAlchemy
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FOLDER: str = os.path.join(BASE_DIR, "assets", "images")
    LOG_FOLDER: str = os.path.join(BASE_DIR, "logs")

    @classmethod
    def init_directories(cls) -> None:
        """Garante a existência física dos diretórios necessários para a aplicação."""
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.LOG_FOLDER, exist_ok=True)

Settings.init_directories()
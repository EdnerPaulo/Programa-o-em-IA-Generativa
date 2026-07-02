"""
Configuração centralizada de logs do sistema.
"""
import logging
import os
from config.settings import Settings

def get_logger(name: str) -> logging.Logger:
    """Retorna um logger configurado para escrita em arquivo e console."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s'
        )
        
        # Handler Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler Arquivo
        log_file = os.path.join(Settings.LOG_FOLDER, "app.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
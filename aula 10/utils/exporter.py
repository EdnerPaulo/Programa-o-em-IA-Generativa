"""
Utilitário para conversão de dados do banco em estruturas exportáveis (CSV, JSON).
"""
import pandas as pd
import json
from typing import List
from models.analise_model import AnaliseModel

class Exporter:
    @staticmethod
    def para_dataframe(analises: List[AnaliseModel]) -> pd.DataFrame:
        """Converte a lista de entidades SQLAlchemy para DataFrame do Pandas."""
        dados = []
        for a in analises:
            dados.append({
                "ID": a.id,
                "Data": a.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Descrição": a.descricao,
                "Objetos": a.objetos,
                "Pessoas": a.quantidade_pessoas,
                "Rostos": a.rostos,
                "Luminosidade": a.luminosidade,
                "Nitidez": a.nitidez,
                "Cores Predominantes": a.cores
            })
        return pd.DataFrame(dados)

    @staticmethod
    def para_json(analises: List[AnaliseModel]) -> str:
        """Exporta os registros em formato JSON textual estruturado."""
        dados = []
        for a in analises:
            dados.append({
                "id": a.id,
                "created_at": a.created_at.isoformat(),
                "metrics": a.json_resultado
            })
        return json.dumps(dados, indent=4, ensure_ascii=False)

from pathlib import Path
import sqlite3
import pandas as pd

# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent

ARQUIVO_BANCO = BASE_DIR / "data" / "crm_analytics.db"
ARQUIVO_SQL = (
    BASE_DIR
    / "sql"
    / "consultas"
    / "01_indicadores_comerciais.sql"
)

print("=" * 60)
print("CRM ANALYTICS - EXECUÇÃO DAS CONSULTAS SQL")
print("=" * 60)

if not ARQUIVO_BANCO.exists():
    raise FileNotFoundError(
        f"Banco não encontrado: {ARQUIVO_BANCO}"
    )

if not ARQUIVO_SQL.exists():
    raise FileNotFoundError(
        f"Arquivo SQL não encontrado: {ARQUIVO_SQL}"
    )

# Lê as consultas do arquivo SQL
conteudo_sql = ARQUIVO_SQL.read_text(encoding="utf-8")

# Separa as consultas pelo ponto e vírgula
consultas = [
    consulta.strip()
    for consulta in conteudo_sql.split(";")
    if consulta.strip()
]

with sqlite3.connect(ARQUIVO_BANCO) as conexao:
    for numero, consulta in enumerate(consultas, start=1):
        print(f"\n{'-' * 60}")
        print(f"CONSULTA {numero}")
        print("-" * 60)

        resultado = pd.read_sql_query(consulta, conexao)
        print(resultado.to_string(index=False))

print("\nTodas as consultas foram executadas!")

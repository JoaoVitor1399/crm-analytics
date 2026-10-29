
from pathlib import Path
import sqlite3
import pandas as pd

# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent

ARQUIVO_CSV = (
    BASE_DIR / "data" / "processed"
    / "base_analise_comercial.csv"
)

ARQUIVO_BANCO = BASE_DIR / "data" / "crm_analytics.db"

print("=" * 55)
print("CRM ANALYTICS - CARGA DO BANCO SQL")
print("=" * 55)

if not ARQUIVO_CSV.exists():
    raise FileNotFoundError(
        f"CSV não encontrado: {ARQUIVO_CSV}"
    )

# Carrega os dados
df = pd.read_csv(ARQUIVO_CSV, encoding="utf-8-sig")

# Remove a coluna auxiliar, se existir
if "É demonstração" in df.columns:
    df = df.drop(columns=["É demonstração"])

# Renomeia as colunas de forma segura
renomear = {
    "ID do registro": "id_registro",
    "Nome Negócio": "nome_negocio",
    "Montante": "montante",
    "Estágio": "estagio",
    "Data de Fechamento": "data_fechamento",
    "Conta Nome.id": "conta_id",
    "Conta Nome": "conta_nome",
    "Nome Contato.id": "contato_id",
    "Nome Contato": "contato_nome",
    "Proprietário do Negócio.id": "proprietario_id",
    "Proprietário do Negócio": "proprietario_nome",
}

df = df.rename(columns=renomear)

# Confere se todas as colunas necessárias existem
colunas_necessarias = list(renomear.values())
faltantes = [
    coluna for coluna in colunas_necessarias
    if coluna not in df.columns
]

if faltantes:
    raise ValueError(
        f"Colunas ausentes no CSV: {faltantes}\n"
        f"Colunas encontradas: {df.columns.tolist()}"
    )

# Ajusta os tipos de dados
df["montante"] = pd.to_numeric(
    df["montante"], errors="coerce"
)

df["data_fechamento"] = pd.to_datetime(
    df["data_fechamento"], errors="coerce"
).dt.strftime("%Y-%m-%d")

# Cria a pasta do banco, se necessário
ARQUIVO_BANCO.parent.mkdir(parents=True, exist_ok=True)

# Carrega os dados no SQLite e executa consultas
with sqlite3.connect(ARQUIVO_BANCO) as conexao:
    df.to_sql(
        "negocios",
        conexao,
        if_exists="replace",
        index=False
    )

    pipeline = pd.read_sql_query(
        """
        SELECT
            COUNT(*) AS quantidade_negocios,
            ROUND(SUM(montante), 2) AS valor_total,
            ROUND(AVG(montante), 2) AS ticket_medio
        FROM negocios
        """,
        conexao
    )

    por_estagio = pd.read_sql_query(
        """
        SELECT
            estagio,
            COUNT(*) AS quantidade,
            ROUND(SUM(montante), 2) AS valor_total
        FROM negocios
        GROUP BY estagio
        ORDER BY valor_total DESC
        """,
        conexao
    )

print(f"\nBanco criado em: {ARQUIVO_BANCO}")
print(f"Registros carregados: {len(df)}")

print("\n1. INDICADORES DO PIPELINE")
print(pipeline.to_string(index=False))

print("\n2. NEGÓCIOS POR ESTÁGIO")
print(por_estagio.to_string(index=False))

print("\nCARGA SQL CONCLUÍDA!")

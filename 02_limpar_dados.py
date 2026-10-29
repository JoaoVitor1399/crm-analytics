
from pathlib import Path
import pandas as pd

# Caminhos do projeto
PASTA_RAW = Path(
    r"C:\Users\João Vitor\Documents\crm-analytics\data\raw"
)

PASTA_PROCESSED = Path(
    r"C:\Users\João Vitor\Documents\crm-analytics\data\processed"
)

PASTA_PROCESSED.mkdir(parents=True, exist_ok=True)

# Localiza o arquivo CSV exportado do Zoho CRM
arquivos = list(PASTA_RAW.glob("*.csv"))

if not arquivos:
    raise FileNotFoundError(
        f"Nenhum CSV encontrado em: {PASTA_RAW}"
    )

arquivo = arquivos[0]

# Lê os dados
try:
    df = pd.read_csv(arquivo, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(arquivo, encoding="latin1")

print("=" * 55)
print("CRM ANALYTICS - LIMPEZA DOS DADOS")
print("=" * 55)

print(f"\nArquivo de origem: {arquivo.name}")
print(f"Registros originais: {len(df)}")

# Padroniza os nomes das colunas
df.columns = df.columns.str.strip()

# Remove espaços extras dos campos de texto
for coluna in df.select_dtypes(include=["object", "str"]).columns:
    df[coluna] = df[coluna].str.strip()

# Converte valores numéricos e datas
df["Montante"] = pd.to_numeric(
    df["Montante"], errors="coerce"
)

df["Data de Fechamento"] = pd.to_datetime(
    df["Data de Fechamento"],
    errors="coerce"
)

# Remove registros sem identificador ou nome do negócio
df = df.dropna(
    subset=["ID do registro", "Nome Negócio"]
)

# Remove registros duplicados pelo identificador
df = df.drop_duplicates(
    subset=["ID do registro"],
    keep="first"
)

# Cria uma coluna para identificar dados de demonstração
colunas_texto = ["Nome Negócio", "Conta Nome", "Nome Contato"]

texto_registro = (
    df[colunas_texto]
    .fillna("")
    .astype(str)
    .agg(" ".join, axis=1)
)

df["É demonstração"] = texto_registro.str.contains(
    r"\(Sample\)",
    case=False,
    regex=True
)

# Separa os negócios de demonstração dos demais
df_demo = df[df["É demonstração"]].copy()
df_reais = df[~df["É demonstração"]].copy()

# Salva as bases tratadas
arquivo_completo = PASTA_PROCESSED / "negocios_tratados.csv"
arquivo_demo = PASTA_PROCESSED / "negocios_demonstracao.csv"
arquivo_reais = PASTA_PROCESSED / "negocios_sem_demo.csv"

df.to_csv(arquivo_completo, index=False, encoding="utf-8-sig")
df_demo.to_csv(arquivo_demo, index=False, encoding="utf-8-sig")
df_reais.to_csv(arquivo_reais, index=False, encoding="utf-8-sig")

# Relatório final
print(f"\nRegistros após limpeza: {len(df)}")
print(f"Negócios de demonstração: {len(df_demo)}")
print(f"Negócios sem indicação de demonstração: {len(df_reais)}")

print("\nValores ausentes:")
print(df.isna().sum().to_string())

print("\nNegócios por estágio:")
print(df["Estágio"].value_counts(dropna=False).to_string())

print("\nArquivos salvos:")
print(f"- {arquivo_completo}")
print(f"- {arquivo_demo}")
print(f"- {arquivo_reais}")

print("\nLIMPEZA CONCLUÍDA!")


from pathlib import Path
import pandas as pd

# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent

ARQUIVO = (
    BASE_DIR
    / "data"
    / "processed"
    / "negocios_sem_demo.csv"
)

PASTA_SAIDA = BASE_DIR / "data" / "processed"
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("CRM ANALYTICS - ANÁLISE COMERCIAL")
print("=" * 60)

# Verifica se o arquivo existe
if not ARQUIVO.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {ARQUIVO}"
    )

# Carrega os dados
df = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

# Converte os campos para os tipos corretos
df["Montante"] = pd.to_numeric(
    df["Montante"], errors="coerce"
)

df["Data de Fechamento"] = pd.to_datetime(
    df["Data de Fechamento"], errors="coerce"
)

# Remove registros sem valor para os cálculos financeiros
df = df.dropna(subset=["Montante"])

# Indicadores gerais
quantidade = len(df)
valor_total = df["Montante"].sum()
ticket_medio = df["Montante"].mean()
mediana = df["Montante"].median()

print("\n1. INDICADORES GERAIS")
print("-" * 40)
print(f"Quantidade de negócios: {quantidade}")
print(f"Valor total do pipeline: R$ {valor_total:,.2f}")
print(f"Ticket médio: R$ {ticket_medio:,.2f}")
print(f"Mediana dos negócios: R$ {mediana:,.2f}")

# Quantidade e valor por estágio
por_estagio = (
    df.groupby("Estágio", dropna=False)
    .agg(
        Quantidade=("ID do registro", "count"),
        Valor_Total=("Montante", "sum"),
        Ticket_Medio=("Montante", "mean")
    )
    .reset_index()
    .sort_values("Valor_Total", ascending=False)
)

print("\n2. ANÁLISE POR ESTÁGIO")
print("-" * 40)
print(por_estagio.to_string(index=False))

# Identifica negócios ganhos e perdidos
estagio = df["Estágio"].fillna("").str.strip().str.lower()

ganhos = estagio.isin(["closed won", "ganho", "fechado ganho"])
perdidos = estagio.isin(["closed lost", "perdido", "fechado perdido"])
encerrados = ganhos | perdidos
em_andamento = ~encerrados

valor_ganho = df.loc[ganhos, "Montante"].sum()
valor_perdido = df.loc[perdidos, "Montante"].sum()
valor_em_andamento = df.loc[em_andamento, "Montante"].sum()

print("\n3. SITUAÇÃO COMERCIAL")
print("-" * 40)
print(f"Negócios ganhos: {ganhos.sum()}")
print(f"Negócios perdidos: {perdidos.sum()}")
print(f"Negócios em andamento: {em_andamento.sum()}")
print(f"Valor ganho: R$ {valor_ganho:,.2f}")
print(f"Valor perdido: R$ {valor_perdido:,.2f}")
print(f"Valor em andamento: R$ {valor_em_andamento:,.2f}")

# Próximos fechamentos previstos
hoje = pd.Timestamp.today().normalize()

proximos = df[
    df["Data de Fechamento"].notna()
    & (df["Data de Fechamento"] >= hoje)
    & em_andamento
].copy()

proximos = proximos.sort_values("Data de Fechamento")

print("\n4. PRÓXIMOS FECHAMENTOS PREVISTOS")
print("-" * 40)

if proximos.empty:
    print("Nenhum fechamento futuro encontrado.")
else:
    print(
        proximos[
            ["Nome Negócio", "Montante", "Estágio", "Data de Fechamento"]
        ].to_string(index=False)
    )

# Exporta os resultados
por_estagio.to_csv(
    PASTA_SAIDA / "indicadores_por_estagio.csv",
    index=False,
    encoding="utf-8-sig"
)

df.to_csv(
    PASTA_SAIDA / "base_analise_comercial.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n5. ARQUIVOS GERADOS")
print("-" * 40)
print("indicadores_por_estagio.csv")
print("base_analise_comercial.csv")

print("\nANÁLISE CONCLUÍDA!")


from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent
PASTA_DADOS = BASE_DIR / "data" / "processed"
PASTA_GRAFICOS = BASE_DIR / "docs" / "graficos"

PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

ARQUIVO = PASTA_DADOS / "base_analise_comercial.csv"

# Configuração visual
sns.set_theme(style="whitegrid", context="talk")

# Carregamento dos dados
if not ARQUIVO.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {ARQUIVO}"
    )

df = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

df["Montante"] = pd.to_numeric(
    df["Montante"], errors="coerce"
)

df["Estágio"] = df["Estágio"].fillna("Não informado")

print("=" * 55)
print("CRM ANALYTICS - VISUALIZAÇÃO DE DADOS")
print("=" * 55)

# Indicadores principais
quantidade = len(df)
valor_total = df["Montante"].sum()
ticket_medio = df["Montante"].mean()

print(f"\nQuantidade de negócios: {quantidade}")
print(f"Valor total do pipeline: R$ {valor_total:,.2f}")
print(f"Ticket médio: R$ {ticket_medio:,.2f}")

# Gráfico 1: valor por negócio
plt.figure(figsize=(12, 7))

dados_valor = df.sort_values("Montante", ascending=False)

ax = sns.barplot(
    data=dados_valor,
    x="Montante",
    y="Nome Negócio",
    hue="Nome Negócio",
    legend=False
)

ax.set_title(
    "Valor das Oportunidades Comerciais",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Valor do negócio (R$)")
ax.set_ylabel("")

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="R$ %.0f",
        padding=5
    )

plt.tight_layout()
plt.savefig(
    PASTA_GRAFICOS / "01_valor_por_negocio.png",
    dpi=200,
    bbox_inches="tight"
)
plt.close()

# Gráfico 2: quantidade de negócios por estágio
contagem = (
    df.groupby("Estágio")
    .size()
    .reset_index(name="Quantidade")
    .sort_values("Quantidade", ascending=False)
)

plt.figure(figsize=(10, 6))

ax = sns.barplot(
    data=contagem,
    x="Estágio",
    y="Quantidade",
    hue="Estágio",
    legend=False
)

ax.set_title(
    "Quantidade de Negócios por Estágio",
    fontsize=18,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Estágio comercial")
ax.set_ylabel("Quantidade")
plt.xticks(rotation=20, ha="right")

for container in ax.containers:
    ax.bar_label(container, padding=4)

plt.tight_layout()
plt.savefig(
    PASTA_GRAFICOS / "02_negocios_por_estagio.png",
    dpi=200,
    bbox_inches="tight"
)
plt.close()

# Gráfico 3: distribuição do valor do pipeline
plt.figure(figsize=(8, 8))

plt.pie(
    df["Montante"],
    labels=df["Nome Negócio"],
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.72
)

plt.title(
    "Participação de Cada Negócio no Pipeline",
    fontsize=17,
    fontweight="bold",
    pad=20
)
plt.tight_layout()
plt.savefig(
    PASTA_GRAFICOS / "03_participacao_pipeline.png",
    dpi=200,
    bbox_inches="tight"
)
plt.close()

print("\nGráficos gerados com sucesso!")

print("\nArquivos salvos em:")
print(PASTA_GRAFICOS)

print("\n1. 01_valor_por_negocio.png")
print("2. 02_negocios_por_estagio.png")
print("3. 03_participacao_pipeline.png")

print("\nVISUALIZAÇÃO CONCLUÍDA!")

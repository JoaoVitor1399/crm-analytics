
from pathlib import Path
import pandas as pd

# Caminho da pasta onde está o CSV exportado do Zoho CRM
pasta_raw = Path(
    r"C:\Users\João Vitor\Documents\crm-analytics\data\raw"
)

print("=" * 55)
print("CRM ANALYTICS - VERIFICAÇÃO DOS DADOS")
print("=" * 55)

# Verifica se a pasta existe
if not pasta_raw.exists():
    print("\nERRO: a pasta não foi encontrada!")
    print(f"Caminho verificado: {pasta_raw}")
else:
    # Localiza todos os arquivos CSV da pasta
    arquivos_csv = list(pasta_raw.glob("*.csv"))

    if not arquivos_csv:
        print("\nERRO: nenhum arquivo CSV encontrado na pasta.")
        print("\nArquivos encontrados nessa pasta:")

        for arquivo in pasta_raw.iterdir():
            print(f"- {arquivo.name}")

        print("\nConfira se o arquivo exportado do Zoho está nessa pasta.")
        print("Se estiver compactado em ZIP, extraia o CSV primeiro.")

    else:
        print("\nArquivos CSV encontrados:")

        for i, arquivo in enumerate(arquivos_csv, start=1):
            print(f"{i}. {arquivo.name}")

        # Lê o primeiro CSV encontrado
        arquivo = arquivos_csv[0]

        try:
            try:
                df = pd.read_csv(arquivo, encoding="utf-8-sig")
            except UnicodeDecodeError:
                df = pd.read_csv(arquivo, encoding="latin1")

            print(f"\nArquivo utilizado: {arquivo.name}")
            print(f"Quantidade de registros: {len(df)}")
            print(f"Quantidade de colunas: {len(df.columns)}")

            print("\nColunas encontradas:")
            print(df.columns.tolist())

            print("\nPrimeiros 5 registros:")
            print(df.head().to_string(index=False))

            print("\nValores ausentes por coluna:")
            print(df.isna().sum().to_string())

            print("\nTipos de dados:")
            print(df.dtypes.to_string())

            print("\nVERIFICAÇÃO CONCLUÍDA!")

        except Exception as erro:
            print("\nERRO AO LER O ARQUIVO:")
            print(erro)

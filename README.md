# CRM Analytics — Análise de Pipeline Comercial

## Sobre o projeto

Projeto de análise de dados comerciais desenvolvido para demonstrar habilidades em **Python, SQL e análise de indicadores de negócio**, utilizando dados exportados do Zoho CRM.

O objetivo é transformar dados brutos de oportunidades comerciais em informações estruturadas que ajudem a analisar o pipeline de vendas, comparar valores por etapa e acompanhar oportunidades com previsão de fechamento.

> **Nota sobre os dados:** este projeto utiliza dados demonstrativos. As quatro oportunidades analisadas foram criadas para fins de portfólio e não representam vendas reais ou receita efetivamente obtida.

## Objetivos

- Desenvolver um processo de limpeza e preparação de dados.
- Identificar e separar registros demonstrativos.
- Calcular indicadores comerciais com Python e SQL.
- Analisar a distribuição do valor das oportunidades.
- Criar visualizações para facilitar a interpretação dos dados.
- Preparar a base para uma futura construção de dashboard no Power BI.

## Tecnologias utilizadas

- **Python:** tratamento, análise e visualização de dados.
- **Pandas:** manipulação de dados tabulares.
- **Matplotlib e Seaborn:** criação de gráficos.
- **SQL:** consultas e indicadores comerciais.
- **SQLite:** armazenamento e consulta dos dados.
- **Power BI:** etapa planejada para desenvolvimento de dashboard.
- **Git e GitHub:** versionamento e publicação do projeto.

## Indicadores analisados

| Indicador | Resultado |
|---|---:|
| Oportunidades analisadas | 4 |
| Valor total do pipeline | R$ 22.700,00 |
| Ticket médio das oportunidades | R$ 5.675,00 |
| Mediana dos valores | R$ 5.500,00 |
| Maior oportunidade | R$ 8.500,00 |
| Menor oportunidade | R$ 3.200,00 |
| Oportunidades em andamento | 4 |

**Atenção:** o valor total representa o valor potencial das oportunidades demonstrativas, não faturamento realizado.

## Principais análises

- Valor potencial total das oportunidades.
- Ticket médio e mediana.
- Distribuição das oportunidades por etapa comercial.
- Ranking de oportunidades por valor.
- Participação percentual de cada oportunidade no pipeline.
- Datas previstas para fechamento.
- Classificação das oportunidades por faixa de valor.

## Estrutura do projeto

```text
crm-analytics/
├── data/
│   ├── raw/
│   │   └── negocios_zoho.csv.csv
│   ├── processed/
│   │   ├── negocios_tratados.csv
│   │   ├── negocios_demonstracao.csv
│   │   ├── negocios_sem_demo.csv
│   │   ├── base_analise_comercial.csv
│   │   └── indicadores_por_estagio.csv
│   └── crm_analytics.db
├── notebooks/
├── sql/
│   └── consultas/
│       └── 01_indicadores_comerciais.sql
├── powerbi/
├── docs/
│   └── graficos/
├── 01_verificar_dados.py
├── 02_limpar_dados.py
├── 03_analise_comercial.py
├── 04_visualizar_dados.py
├── 05_carregar_sql.py
├── 06_executar_consultas_sql.py
└── README.md
```

*Observação: a estrutura e os nomes dos arquivos podem evoluir durante o desenvolvimento.*

## Como executar

### 1. Clonar o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
cd crm-analytics
```

Substitua `URL_DO_SEU_REPOSITORIO` pelo endereço do repositório criado no GitHub.

### 2. Criar e ativar o ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install pandas matplotlib seaborn sqlalchemy
```

### 4. Executar os scripts

Na ordem:

```bash
python 01_verificar_dados.py
python 02_limpar_dados.py
python 03_analise_comercial.py
python 04_visualizar_dados.py
python 05_carregar_sql.py
python 06_executar_consultas_sql.py
```

Execute os comandos na pasta principal do projeto. O arquivo CSV exportado do Zoho CRM deve estar na pasta `data/raw/`.

## Próximas melhorias

- Construir um dashboard interativo no Power BI.
- Criar indicadores de conversão entre etapas do funil.
- Comparar oportunidades por período.
- Automatizar a atualização dos dados.
- Documentar os resultados com capturas do dashboard.
- Publicar o projeto com versionamento no GitHub.

## Autor

Projeto desenvolvido para portfólio profissional na área de **Análise de Dados**.
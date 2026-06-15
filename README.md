# DBT Stocks Pipeline

ELT pipeline completo para análise de dados de ações do mercado financeiro americano.

## Sobre o projeto

Empresas modernas de dados não transformam dados antes de carregá-los no warehouse — elas carregam tudo primeiro e transformam depois. Esse padrão se chama ELT (Extract, Load, Transform), e o dbt é a ferramenta padrão de mercado para o T dessa equação.

Este projeto simula um pipeline real de engenharia de dados para o mercado financeiro. Dados de 5 ações americanas são extraídos da API do yfinance, carregados em um PostgreSQL containerizado com Docker, e transformados em camadas organizadas com dbt — o mesmo fluxo usado por times de dados em empresas que operam com Snowflake, BigQuery ou Redshift.

O objetivo foi cobrir o máximo de conceitos do dbt em um projeto com contexto real: desde a ingestão até a camada de consumo pronta para um dashboard em Power BI ou Looker.

## Por que dbt?

Em ambientes corporativos com AWS, Azure ou GCP, o dbt entra após as ferramentas de ingestão (Fivetran, Airbyte, Glue) e atua dentro do warehouse — organizando, testando e documentando as transformações SQL. Ele não substitui essas ferramentas, complementa. O resultado é um pipeline versionado no Git, com testes de qualidade declarativos e documentação gerada automaticamente — algo que procedures SQL legadas jamais entregam.

## Stack

- **Python** + yfinance — ingestão de dados reais de mercado
- **PostgreSQL** — warehouse local
- **Docker** — containerização do ambiente
- **dbt** — transformação e modelagem dos dados

## Arquitetura
yfinance API → Python (ingest.py) → PostgreSQL → dbt → mart_stock_daily

### Camadas dbt

| Camada | Model | Descrição |
|---|---|---|
| Source | raw_stock_prices | Dados brutos ingeridos via Python |
| Staging | stg_stock_prices | Padronização de colunas e tipos |
| Intermediate | int_stock_metrics | Métricas derivadas: variação, range, direção |
| Mart | mart_stock_daily | Visão final enriquecida com dados da empresa |

## Conceitos dbt cobertos

- Sources e `source()`
- Models com `ref()`
- Materializations: `view` e `table`
- Generic tests: `not_null`, `accepted_values`
- Singular tests customizados
- Seeds — tabela de referência de empresas
- Macros — função reutilizável `round_numeric()`
- Snapshots — SCD Tipo 2 em `companies_snapshot`
- Documentação com `dbt docs`

## Como rodar

### Pré-requisitos

- Docker Desktop
- Python 3.13+
- dbt-core 1.8 + dbt-postgres 1.8

### 1. Sobe o banco

```bash
docker-compose up -d
```

### 2. Instala dependências Python

```bash
cd ingestion
pip install -r requirements.txt
```

### 3. Configura variáveis de ambiente

Cria um `.env` na raiz com:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=financeiro
DB_USER=dbt_user
DB_PASS=dbt_pass
```

### 4. Ingere os dados

```bash
python ingest.py
```

### 5. Roda o dbt

```bash
cd ../dbt_stocks
dbt seed
dbt run
dbt test
dbt snapshot
```

### 6. Documentação

```bash
dbt docs generate
dbt docs serve
```

## Ações cobertas

| Ticker | Empresa |
|---|---|
| IBM | International Business Machines |
| AAPL | Apple Inc |
| MSFT | Microsoft Corporation |
| GOOGL | Alphabet Inc |
| AMZN | Amazon.com Inc |

## Autor

Victor Araujo — [LinkedIn](www.linkedin.com/in/victor-lucas-dataengineer) · [GitHub](https://github.com/Victoraraujo965)

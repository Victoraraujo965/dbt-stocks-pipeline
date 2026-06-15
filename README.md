# dbt Stocks Pipeline

ELT pipeline completo para análise de dados de ações do mercado financeiro americano.

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
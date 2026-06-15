with stg as (
    select * from {{ ref('stg_stock_prices') }}
),

metrics as (
    select
        symbol,
        date,
        price_open,
        price_close,
        price_high,
        price_low,
        volume,

        {{ round_numeric('price_close - price_open') }}           as daily_change,
        {{ round_numeric('(price_close - price_open) / price_open * 100') }} as daily_change_pct,
        {{ round_numeric('price_high - price_low') }}             as daily_range,

        -- Classificação do dia
        case
            when price_close > price_open then 'alta'
            when price_close < price_open then 'baixa'
            else 'neutro'
        end as day_direction,

        -- Métricas mensais via window function
        round(avg(price_close) over (
            partition by symbol, date_trunc('month', date)
        )::numeric, 2) as avg_close_month,

        round(sum(volume) over (
            partition by symbol, date_trunc('month', date)
        )::numeric, 0) as total_volume_month

    from stg
)

select * from metrics
with int as (
    select * from {{ ref('int_stock_metrics') }}
),

companies as (
    select * from {{ ref('companies') }}
),

final as (
    select
        i.symbol,
        c.company_name,
        c.sector,
        c.country,
        i.date,
        i.price_open,
        i.price_close,
        i.price_high,
        i.price_low,
        i.volume,
        i.daily_change,
        i.daily_change_pct,
        i.daily_range,
        i.day_direction,
        i.avg_close_month,
        i.total_volume_month,
        now() as loaded_at

    from int i
    left join companies c on i.symbol = c.symbol
)

select * from final
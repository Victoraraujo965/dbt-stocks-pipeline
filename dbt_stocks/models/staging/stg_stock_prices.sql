with source as (
    select * from {{ source('public', 'raw_stock_prices') }}
),

renamed as (
    select
        symbol,
        date,
        open    as price_open,
        high    as price_high,
        low     as price_low,
        close   as price_close,
        volume
    from source
)

select * from renamed
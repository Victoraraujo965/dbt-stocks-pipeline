select *
from {{ ref('mart_stock_daily') }}
where price_close <= 0
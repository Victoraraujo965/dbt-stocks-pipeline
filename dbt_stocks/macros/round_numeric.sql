{% macro round_numeric(column, decimals=2) %}
    round(({{ column }})::numeric, {{ decimals }})
{% endmacro %}
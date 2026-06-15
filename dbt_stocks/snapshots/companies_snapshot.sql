{% snapshot companies_snapshot %}

{{
    config(
        target_schema='public',
        unique_key='symbol',
        strategy='check',
        check_cols=['sector', 'company_name', 'country']
    )
}}

select * from {{ ref('companies') }}

{% endsnapshot %}
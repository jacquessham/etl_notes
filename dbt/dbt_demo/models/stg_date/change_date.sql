with dates as (

	select * from {{ ref('stg_source') }}
)

select ts::date from dates
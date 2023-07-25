{% set commute_expenses = ["transportation", "toll"] %}



select name, 
	{% for commute_expense in commute_expenses %}
	sum(case when expense_category = '{{commute_expense}}' then {{ dollars2yen('total_amount') }} else 0 end)
		as {{commute_expense}}_amount_jpy,
	{% endfor %}
	sum(total_amount) as total_amount_usd
from {{ref('total_amount')}}
group by 1
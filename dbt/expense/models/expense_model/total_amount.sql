select name, expense_category, sum(amount) as total_amount
from {{ source('expense_source','expense_everybody')}}
group by 1, 2
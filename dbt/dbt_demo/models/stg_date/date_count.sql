select username, year, month, count(1) as date_count
from 
{{ ref('date_parse')}}
group by 1,2,3
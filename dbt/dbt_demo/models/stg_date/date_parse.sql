select date_part('year',ts::timestamp) as year,
	date_part('month', ts::timestamp) as month,
	ts, username
from testing.df_testing
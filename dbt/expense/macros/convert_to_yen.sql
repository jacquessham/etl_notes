{% macro dollars2yen(col_name) %}
	round( {{ col_name }} * 140)
{% endmacro %}
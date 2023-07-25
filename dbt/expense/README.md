# Expense (dbt Demo 2)
In this dbt Project, we will experiment some advanced dbt features. At this point, you are expected to have <i>profile.yml</i> prepared.

## Seed
We have a CSV file <i>expense_everybody.csv</i> as a sample dataset to be uploaded to the database. First, fill in the configuration in the Project Yaml file like below:

```
...

seeds: # Seed
  expense: # Project Name
    expense_everybody: # Table Name
      name: varchar(512) # Column name and data type
      expense_category: varchar(512)
      amount: numeric(12,2)

...

```

This portion of the metadata will define the DDL automatically.
<br><br>
We can execute the following code on the command line to trigger the upload:

```
dbt seed
```
<br>
After the execution finished sucessfully, you may check the table under the schema stated in the <i>profile.yml</i> file.

## Models
Here are all the SQL scripts in the <i>models</i> folder:
* total_amount.sql
* everybody_totalexpense.sql


<br>
we have <i>total_amount.sql</i> as a CTE script to sum the total expense by each person and his expense category. This is an example to reference the <i>sources</i>
stated in the Model Yaml file. Here is what we have in the Model Yaml file and the script:

```
version: 2

sources:
  - name: expense_source
    database: spotify
    schema: testing
    tables:
      - name: expense_everybody

models:
  - name: everybody_totalexpense
```

```
select name, expense_category, sum(amount) as total_amount
from {{ source('expense_source','expense_everybody')}}
group by 1, 2
```

<i>expense_source</i> and <i>expense_everybody</i> in the SQL script is mapped to the source name stated in <i>schema.yml</i>.

### Jinja
You may utilize Jinja syntax to use a for loop or if statement in Python when creating your SQL syntax. For example, you may use this when creating mulitple similar case when value equal to something for mulitple time, like below:

```
{% set commute_expenses = ["transportation", "toll"] %}

select name, 
	{% for commute_expense in commute_expenses %}
	sum(case when expense_category = '{{commute_expense}}' then total_amount else 0 end)
		as {{commute_expense}}_amount,
	{% endfor %}
	sum(total_amount) as total_amount
from {{ref('total_amount')}}
group by 1
```
<br>
It means I would decleare a Python list in this SQL script and create the expense type as column in a Python style for loop. <b>Note: The for loop do not take care the comma(,) automatically for you! So you have to include in the loop, that means you need an extra hardcoded column at the end to prevent syntax error of placing comma(,) before the from component...</b>

### Macros
you may utilize Macros to build a function. First, define the Macros under the <i>macros</i> folder and write a Macro in a SQL script, like below:

```
{% macro dollars2yen(col_name) %}
	round( {{ col_name }} * 140)
{% endmacro %}
```

<br>
However, beware that the arguement pass is directly pass into the SQL script. It means, it is not possible to pass a constant value to the Macro itself to make a calculation between a column and a constant value. For example, if we have:

```
{% macro dollars2yen(col_name, ex_rate) %}
	round( {{ col_name }} * ex_rate)
{% endmacro %}

```

dbt would have compiled to multiplication between two columns, and so far there is no way to indicate ex_rate is a constant value yet. 
# dbt
dbt is a transformation tool that allows you to build the data pipeline with Jinja format and SQL scripts. It is a tool for you if your pipeline is heavily rely on SQL scripts for transformation.

## Quick Start
Before getting your hands dirty on dbt, you should have a database ready. In this project, we will be using Postgres. We have two projects: [dbt_demo](/dbt_demo) and [Expense](/expense) to demostrate the basic and advance use cases of dbt.

### Steps to Prepare Prerequisites and Execution
1. Upgrade Python > 3.8
2. Create environment
3. Install dbt, along with database adapter
4. Update profile.yaml
5. Initiate dbt project folder
6. Prepare models (SQL scripts)
7. Test dbt
8. Run dbt

### Create Environment
The first step is to create a Python enviornment, ensure the Python version > 3.8, and install all necessary dependences.

```
python -m venv [env_name]
```

### Install dbt
Installing dbt-core and your dbt adapter, but install your dbt adapter will automatically install dbt-core right away.

```
pip install [dbt-postgres/adapter]
```

### Update profile.yaml
Under /user/username/.dbt, open profile.yaml. Fill in the database credentials. An example is 

```
dbt_demo:
  outputs:
    dev:
      type: postgres
      threads: 1
      host: localhost
      port: 5432
      user: some_user
      pass: some_password
      dbname: some_db
      schema: testing
    prod:
      type: postgres
      threads: 1
      host: localhost
      port: 5432
      user: some_user
      pass: some_password
      dbname: some_db
      schema: testing
  target: dev

```

### Initiate dbt project
Under the desired directory

```
dbt init [project_name]
```

<br>
Every time you initiate a new dbt project, you would need to fill in the database credentials in <i>profile.yaml</i>.
<br><br>
Once the project is initiated, it would generate a Project Yaml file in <i>[project_name].yml</i>. You would need to fill in the configuration for your dbt project. You may use the generated Project Yaml file and add and take out the desired metadata for your needs.

### Seed
Seed is the feature of dbt to upload data from CSV to the targeted database. First, you have to state the configuration in Project Yaml file. An example is:

```
...

seeds:
  expense:
    expense_everybody:
      name: varchar(512)
      expense_category: varchar(512)
      amount: numeric(12,2)

...
```

You may find the this example in the [Expense](/expense) Project folder.


### Prepare models (SQL scripts)
Go to the model folder, create a new folder and write the SQL scripts. <b>In the model subfolders, be sure to include <i>schema.yml</i> for the model configuration, or else it would fail.</b> An example of the folder structure should look like this:

```
- Project_name
| - ...
| - ...
| - models
  | - sub_model
  	| - SQL script 1
  	| - ...
  	| - SQL script N
  	| - schema.yml
```
<br>
An example of a <i>schema.yml</i> is:

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
<br>
Having those configuration is necessary to utilize Jinja reference, such as <i>sources</i>, like the following SQL script:

```
select name, expense_category, sum(amount) as total_amount
from {{ source('expense_source','expense_everybody')}}
group by 1, 2
```

Note: <i>expense_source</i> and <i>expense_everybody</i> in the SQL script is mapped to the source name stated in <i>schema.yml</i>.

### Run Test
You may run test to assert your models and other resource, dbt will tell you if each test in your project passes or fails. There are two ways of defining test: <i>singular</i> and <i>generic</i>.
<br><br>
* Singular Test: Simplest form. It test a SQL query and returns failing rows
* Generic Test: Parametrized query that accepts arguments defined in the Yaml files.
<br><br>
If so, execute:

```
dbt test
```

### Run dbt
Change directory to the project folder, run:

```
dbt run
```

## Tips
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

### Macros
you may utilize Macros to build a function. First, define the Macros under the <i>macros</i> folder and write a Macro in a SQL script, like below:

```
{% macro dollars2yen(col_name) %}
	round( {{ col_name }} * 140)
{% endmacro %}
```



## Reference
<a href="https://docs.getdbt.com/docs/introduction">dbt Documentation</a>
<a href="https://youtu.be/toSAAgLUHuk">Run Locally</a>
<a href="https://youtu.be/mSXuh0szBGk">Run in Docker</a>
# dbt_demo (dbt Demo 1)
In this dbt Project, we will experiment the basic dbt features: Initiate dbt Projects, Models and Tests.

## Prepare Prerequisites
### Create Environment

The first step is to create a Python enviornment, ensure the Python version > 3.8, and install all necessary dependences.

```
python -m venv [env_name]
```

Once you have created an environment, you may activate with it:

```
source [env_name]/bin/activate
```

It is also wise to upgrade pip:

```
pip install --upgrade pip
```

### Install dbt
Installing dbt-core and your dbt adapter, but install your dbt adapter will automatically install dbt-core right away. If Python version is not 3.8 or newer, dbt is not supported and the pip install would fail.

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

## Understand the Folder Structure
Once you have initiate the projects, dbt would create a folder with all the necessary subfolders in it, each subfolder represents its feature. Here is a typical dbt folder structure looks like:

```
[project_name]
 |- analyses
 |- macros
 |- models
 |- seeds
 |- snapshots
 |- tests
```

We will focus with <i>models</i> and <i>tests</i> and discuss <i>seeds</i> and <i>macros</i> in the [Expense](../Expense) section.

### Models
Models are defined in SQL scripts in dbt, you may think of models represents database properties like table, views, and so on. The configuration is defined in <i>schema.yml</i> in the its subfolders, it is where you define what SQL scripts you want to materialize as table or view. The best part is that it automatically create table and insert data for you. An example of <i>schema.yml</i> from dbt is:

```
version: 2

models:
  - name: my_first_dbt_model
    description: "A starter dbt model"
    columns:
      - name: id
        description: "The primary key for this table"
        tests:
          - unique
          - not_null

  - name: my_second_dbt_model
    description: "A starter dbt model"
    columns:
      - name: id
        description: "The primary key for this table"
        tests:
          - unique
          - not_null
```

This yml files specifically create two views, and ensure columns id from both views to be unique and not_null. As we have mentioned those models are materialized as view because it is defined in <i>dbt_project.yml</i> in the project folder:

```
models:
  dbt_demo:
    # Config indicated by + and applies to all files under models/example/
    example:
      +materialized: view
    materialized: table
```

It says that in the <i>models/example</i> subfolder, all models will be materialized as view, which also applies to downstream subfolder because there is a <b>+</b> sign to indicate that.
<br><br>
You may see that any other models outside of the <i>models/example</i> subfolder are materialized as table. Therefore, any SQL scripts written in <i>models/stg_date</i> will be materialize as table. Note that, there is no <i>schema.yml</i> defined here is still allowed, however, only generic configuration and test are applied to these models in this subfolder.
<br><br>
Let's take a step back to <i>my_first_dbt_model.sql</i>. Since it is saved under the <i>models/example</i> subfolder, the model is expected to be materialized as view. However, there is a line of code to override that model to be materialized as table:

```
{{ config(materialized='table') }}

...
```

Another best part about dbt is that dbt does a lot of setup works for you -- You don't have to create table and insert into, simply write a select statement to insert data into a new table. The table name is based on the SQL script filename or the name define in <i>schema.yml</i>.
<br><br>
Last advantage using dbt is utilizing Jinja for referencing other models or objects defined in the project. For example, you may reference from another model like in <i>my_second_dbt_model.sql</i>:

```
select *
from {{ ref('my_first_dbt_model') }}
where id = 1

```

So that you don't have to copy and paste the work from another script to prevent logically errors and easy reference from a number of existing works.

### Test
You may run test to assert your models and other resource, dbt will tell you if each test in your project passes or fails. There are two ways of defining test: <i>singular</i> and <i>generic</i>.
<br><br>
* Singular Test: Simplest form. It test a SQL query and returns failing rows
* Generic Test: Parametrized query that accepts arguments defined in the Yaml files.
<br><br>
When you trigger the test function, dbt would compile the SQL scripts and saved under the <i>test</i>. If you have received error message after triggered a dbt test, it would point you to this folder to debug you SQL scripts. 
<br><br>
If you want to test the integrity of the model, you may utilize a generic test with dbt. You may specify whether you want to check whether a column is:
* unique: Unique value 
* not_null: Not null
* accepted_values: An array of accepted values
* relationship: Referential Integrity - whether this foreign key can be reference from a primary key of another table

<br>
In order to do this, you would defined in the <i>schema.yml</i> in the <i>models</i> folder, here is the example from dbt documentation:

```
version: 2

models:
  - name: orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['placed', 'shipped', 'completed', 'returned']
      - name: customer_id
        tests:
          - relationships:
              to: ref('customers')
              field: id

```


<br><br>
After you have define the configuration. You may trigger a dbt test by executing:

```
dbt test
```




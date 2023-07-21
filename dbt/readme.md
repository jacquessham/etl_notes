# dbt
Coming soon...

## Quick Start

### Prerequisite
1. Upgrade Python > 3.8
2. Create environment
3. Install dbt, along with database adapter
4. Update profile.yaml
5. Initiate dbt project folder
6. Prepare models (SQL scripts)
7. Run dbt

### Create Environment

```
python -m venv [env_name]
```

### Install dbt

```
pip install [dbt-postgres/adapter]
```

### Update profile.yaml
Under /user/username/.dbt, open profile.yaml. Fill in the database credentials.

### Initiate dbt project
Under the desired directory

```
dbt init [project_name]
```

### Prepare models (SQL scripts)
Go to the model folder, create a new folder and write the SQL scripts.

### Run dbt
Change directory to the project folder, run:

```
dbt run
```

## Reference
<a href="https://youtu.be/toSAAgLUHuk">Run Locally</a>
<a href="https://youtu.be/mSXuh0szBGk">Run in Docker</a>
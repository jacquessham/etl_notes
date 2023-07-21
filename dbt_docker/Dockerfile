FROM python:3.7-slim-buster

RUN apt-get update \
	&& apt-get install -y --no-install-recommends

WORKDIR /usr/src/dbt/dbt_projects

# Update pip
RUN pip install --upgrade pip

# Install dbt Postgres adapter and dbt-core in one command
RUN pip install dbt-core
RUN pip install dbt-postgres

# Install dbt dependencies
CMD dbt deps && dbt build --profiles-dir profiles && sleep infinity

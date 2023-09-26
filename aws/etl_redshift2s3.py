import psycopg2


# Connect with Redshift via psycopg2
user = 'some_username'
password = 'some_password'
redshift_host = 'somedomain.us-west-2.redshift.amazonaws.com'
demo_dbname = 'some_dbname'

conn = psycopg2.connect("dbname=demo_dbname \
host=redshift_host \
port=5439 \
user={} \
password='{}'".format(user, password))

cur = conn.cursor()


# Unload to s3 bucket
# https://stackoverflow.com/questions/20323919/how-to-unload-a-table-on-redshift-to-a-single-csv-file
aws_access_key_id = 'some_access_key'
aws_secret_access_key = 'some_secret_key'

unload_sql="""unload ('SELECT count(*) from some_schema.some_table')
    to 's3://some_domain/some_folder'
    credentials
    'aws_access_key_id={};aws_secret_access_key={}'
    parallel off;
    """.format(aws_access_key_id, aws_secret_access_key)

cur.execute(unload_sql)
conn.commit()
print("Saved data to S3 bucket")

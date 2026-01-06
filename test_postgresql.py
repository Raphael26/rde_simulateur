import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="zromain",
    password="azerty123",
    host="localhost",
    port="5432"
)
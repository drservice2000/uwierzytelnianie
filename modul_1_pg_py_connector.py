# polaczenie z baza danych Postgressql
import psycopg2

def ConnectionPG(host, database, user, password):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password)
    return connection

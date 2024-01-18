
import psycopg2
import torch
import os
import matplotlib.pyplot as plt
import sys

################### Connection with database #######################
def ConnectionPG(host,database,user,password):
    conn = psycopg2.connect(host=host,database=database,user=user,password=password)
    return conn

host = "localhost"
database = "uwierzytelnianie"
user = "postgres"
password = "PasswordPSQL"

# połaczenie z baza danych
PG = ConnectionPG(host,database,user,password)
####### test connecton ###############
cursor = PG.cursor()
cursor.execute("SELECT * FROM uzytkownicy")
for row in cursor:
    print(row)
PG.close()
#####################################################################




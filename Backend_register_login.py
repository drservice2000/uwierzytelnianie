from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql
import bcrypt
from datetime import datetime

app = Flask(__name__)

# Połączenie z bazą danych
conn = psycopg2.connect(
    database="uwierzytelnianie",
    user="postgres",
    password="PasswordPSQL",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Utworzenie tabeli, jeśli nie istnieje
create_table_query = """
CREATE TABLE IF NOT EXISTS uzytkownicy
(
    id_user smallserial PRIMARY KEY,
    firstname VARCHAR (50) UNIQUE NOT NULL,
    lastname VARCHAR (70) UNIQUE NOT NULL,
    password VARCHAR (255) NOT NULL,
    email VARCHAR (255) UNIQUE NOT NULL,
    path_of_vaw VARCHAR (250) UNIQUE NULL,
    uzytkownika_dodano DATE NOT NULL DEFAULT CURRENT_DATE,
    ostatnie_logowanie DATE NOT NULL DEFAULT CURRENT_DATE
);
"""
cursor.execute(create_table_query)
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    password = request.form['password']
    email = request.form['email']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    insert_query = sql.SQL("""
    INSERT INTO uzytkownicy (firstname, lastname, password, email)
    VALUES ({}, {}, {}, {})
    RETURNING id_user;
    """).format(
        sql.Literal(firstname),
        sql.Literal(lastname),
        sql.Literal(hashed_password.decode('utf-8')),
        sql.Literal(email)
    )

    cursor.execute(insert_query)
    user_id = cursor.fetchone()[0]
    conn.commit()

    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    select_query = sql.SQL("""
    SELECT id_user, password FROM uzytkownicy WHERE email = {};
    """).format(sql.Literal(email))

    cursor.execute(select_query)
    result = cursor.fetchone()

    if result:
        user_id, hashed_password = result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return f"Zalogowano użytkownika o ID: {user_id}"

    return "Błąd logowania"

if __name__ == '__main__':
    app.run(debug=True)

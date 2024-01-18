from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/uwierzytelnianie'
db = SQLAlchemy(app)

class User(db.Model):
    id_user = db.Column(db.SmallInteger, primary_key=True)
    firstname = db.Column(db.String(50), unique=True, nullable=False)
    lastname = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    path_of_vaw = db.Column(db.String(250), unique=True, nullable=True)
    uzytkownika_dodano = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    ostatnie_logowanie = db.Column(db.Date, nullable=False, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        email = request.form['email']

        new_user = User(firstname=firstname, lastname=lastname, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

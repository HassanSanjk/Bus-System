from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Hassan@Sanjk7",
        database = "bus_system_db"
    )

app = Flask(__name__)
app.secret_key = "SECRET_KEY"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        con.close()

        if user:
            session["user_id"] = user[0]
            return redirect(url_for("dashboard", name = user[1]))

    return render_template('login.html')


@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password1']
        phone = request.form['phone']


        con = db_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO users (name, email, password, phone, role) VALUES (%s, %s, %s, %s, 'user')", (name, email, password, phone))
        con.commit()
        con.close()

        return redirect(url_for("login"))

    return render_template('signup.html')


@app.route('/dashboard/<name>')
def dashboard(name):
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html', name = name)



if __name__ == '__main__':
    app.run(debug = True)
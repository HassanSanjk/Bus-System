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
        user = cursor.fetchone(dictionary = True)
        con.close()

        if user:
            session["user_id"] = user['id']
            return redirect(url_for("dashboard", name = user['name']))

    return render_template('login.html')


@app.route('/register', methods = ['POST','GET'])
def register():
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

    return render_template('register.html')


@app.route('/dashboard/<name>')
def dashboard(name):
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html', name = name)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.route('/drivers', methods = ['GET','POST'])
def drivers():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        license_number = request.form['license_number']
        phone = request.form['phone']
        experience = request.form['experience']
        status = request.form['status']

        con = db_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO drivers (name, license_number, phone, experience, status) VALUES (%s, %s, %s, %s, %s)", (name, license_number, phone, experience, status))
        con.commit()
        con.close()

    con = db_connection()
    cursor = con.cursor(dictionary = True)
    cursor.execute("SELECT * FROM users WHERE role = 'driver'")
    drivers = cursor.fetchall()
    con.close()

    return render_template('drivers.html', drivers = drivers)

@app.route('/add_bus', methods = ['GET','POST'])
def add_bus():
    if 'user_id' not in session:
        return redirect('/login')


@app.route('/routes', methods = ['GET','POST'])
def add_route():
    if 'user_id' not in session and session['role'] != 'admin':
        return redirect('/login')
    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        distance = request.form['distance']
        travel_time = request.form['travel_time']

        con = db_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO routes (start, destination, distance_km, travel_time) VALUES (%s, %s, %s, %s)", (start, destination, distance, travel_time))
        con.commit()
        con.close()
    con = db_connection()
    cursor = con.cursor(dictionary = True)
    cursor.execute("SELECT * FROM routes")
    routes = cursor.fetchall()
    con.close()
    return render_template('routes.html', routes = routes)


@app.route('/schedules', methods = ['GET','POST'])
def add_schedule():
    if 'user_id' not in session and session['role'] != 'admin':
        return redirect('/login')
    if request.method == 'POST':
        bus_id = request.form['bus_id']
        route_id = request.form['route_id']
        departure_time = request.form['departure_time']
        arriving_time = request.form['arriving_time']
        price = request.form['price']

        con = db_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO schedules (bus_id, route_id, departure_time, arriving_time, price) VALUES (%s, %s, %s, %s, %s)", (bus_id, route_id, departure_time, arriving_time, price))
        con.commit()
        con.close()
        
    con = db_connection()
    cursor = con.cursor(dictionary = True)
    cursor.execute("SELECT * FROM schedules")
    schedules = cursor.fetchall()
    con.close()
    return render_template('schedules.html', schedules = schedules)

@app.route('/book', methods = ['GET','POST'])
def book():
    if 'user_id' not in session:
        return redirect('/login')
    
#payment
@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug = True)
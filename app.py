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

@app.route('/bookings', methods = ['GET','POST'])
def bookings():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        user_id = session['user_id']
        schedule_id = request.form['schedule_id']
        seat_number = request.form['seat_number']
        status = 'booked'
        booking_time = request.form['booking_time']

        con = db_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO bookings (user_id, schedule_id, seat_number, status, booking_time) VALUES (%s, %s, %s, %s, %s)", (user_id, schedule_id, seat_number, status, booking_time))
        con.commit()
        con.close()

    con = db_connection()
    cursor = con.cursor(dictionary = True)
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    con.close()

    return render_template('bookings.html', bookings = bookings)

@app.route("/bookings/delete/<int:booking_id>")
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    con = db_connection()
    cursor = con.cursor()
    cursor.execute("UPDATE bookings SET status = 'cancelled' WHERE id = %s AND user_id = %s", (booking_id, session['user_id']))
    con.commit()
    con.close()

    return redirect(url_for('bookings'))

@app.route('/busses', methods = ['GET', 'POST'])
def busses():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        bus_number = request.form['bus_number']
        seats_number = request.form['seats_number']
        colour = request.form['colour']
        driver_id = request.form['driver_id']

        con = db_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO busses (bus_number, seats_number, colour, driver_id) VALUES (%s, %s, %s, %s)", (bus_number, seats_number, colour, driver_id))
        con.commit()
        con.close()

    con = db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM busses")
    busses = cursor.fetchall()
    con.close()

    return render_template('busses.html', busses = busses)

@app.route('/')
    
#payment
@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug = True)
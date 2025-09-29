from flask import Flask, render_template, redirect, session, Blueprint, request, url_for
from db import db_connection
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')


@views_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""select r.start as start,
r.destination as destination,
s.departure_time as departure_time,
b.bus_number as bus_number,
bk.seat_number as seat_number,
bk.status as status
from bookings bk
join schedules s on bk.schedule_id = s.id
join routes r on s.route_id = r.id
join buses b on s.bus_id = b.id
where bk.user_id = %s and s.departure_time > NOW()
order by s.departure_time;""" , (session["user_id"],))
    upcoming_bookings = cursor.fetchall()
    db.close()

    return render_template('dashboard.html', name = session['name'], upcoming_bookings = upcoming_bookings)


@views_bp.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        due_date = request.form['due_date']

        db = db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO bookings (user_id, schedule_id, seat_number, status, booking_time) VALUES (%s, %s, %s, %s, NOW())",(session['user_id'], title, due_date))
        db.commit()
        db.close()

        return redirect(url_for('views.dashboard'))

    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schedules WHERE departure_time > NOW()")
    schedules = cursor.fetchall()
    db.close()

    return render_template('add_booking.html', schedules=schedules)
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from db import db_connection

bookings_bp = Blueprint('bookings',__name__)


@bookings_bp.route('/bookings', methods = ['GET','POST'])
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

@bookings_bp.route("/bookings/delete/<int:booking_id>")
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    con = db_connection()
    cursor = con.cursor()
    cursor.execute("UPDATE bookings SET status = 'cancelled' WHERE id = %s AND user_id = %s", (booking_id, session['user_id']))
    con.commit()
    con.close()

    return redirect(url_for('bookings'))


@bookings_bp.route('/payment', methods = ['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        return redirect('/login')

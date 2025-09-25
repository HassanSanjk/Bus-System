from flask import Flask, render_template, request, redirect, session, Blueprint
from db import db_connection

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/routes', methods = ['GET','POST'])
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




@routes_bp.route('/schedules', methods = ['GET','POST'])
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


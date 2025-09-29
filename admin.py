from flask import Flask, render_template, request, redirect, session, Blueprint, url_for
from db import db_connection

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/routes')
def manage_routes():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM routes")
    routes = cursor.fetchall()
    db.close()

    return render_template('routes.html', routes=routes)

@admin_bp.route('/add_route', methods=['GET', 'POST'])
def add_route():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        distance = request.form['distance']
        hours = request.form['hours']
        minutes = request.form['minutes']

        travel_time = f"{hours:02}:{minutes:02}:00"

        db = db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO routes (start, destination, distance, duration) VALUES (%s, %s, %s, %s)",
                       (start, destination, distance, travel_time))
        db.commit()
        db.close()

        return redirect(url_for('views.manage_routes'))

    return render_template('add_route.html')

@admin_bp.route('/delete_route/<int:route_id>')
def delete_route(route_id):
    if 'user_id' not in session:
        return redirect('/login')
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM routes WHERE id = %s AND user_id = %s", (route_id, session['user_id']))
    db.commit()
    return redirect(url_for('admin.manage_routes'))


@admin_bp.route('/schedules')
def manage_schedules():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""select b.bus_number as bus_number, s.bus_id as bus_id,
                    s.departure_time as departure_time, s.arriving_time as arriving_time,
                    s.price as price from buses b join schedules s on s.bus_id = b.id;""")
    schedules = cursor.fetchall()
    db.close()

    return render_template('schedules.html', schedules=schedules)

@admin_bp.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']

        db = db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO routes (start, destination, distance, duration) VALUES (%s, %s, %s, %s)",
                       (start, destination, distance, travel_time))
        db.commit()
        db.close()

        return redirect(url_for('views.manage_routes'))

    return render_template('add_route.html')

@admin_bp.route('/delete_schedule/<int:schedule_id>')
def delete_schedule(schedule_id):
    if 'user_id' not in session:
        return redirect('/login')
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM schedules WHERE id = %s AND user_id = %s", (schedule_id, session['user_id']))
    db.commit()
    return redirect(url_for('admin.manage_schedules'))



@admin_bp.route('/buses')
def manage_buses():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM buses")
    buses = cursor.fetchall()
    db.close()

    return render_template('buses.html', buses=buses)

@admin_bp.route('/add_bus', methods=['GET', 'POST'])
def add_bus():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        db = db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO routes (start, destination, distance, duration) VALUES (%s, %s, %s, %s)",
                       (start, destination, distance, travel_time))
        db.commit()
        db.close()

        return redirect(url_for('views.manage_routes'))

    return render_template('add_route.html')

@admin_bp.route('/delete_bus/<int:bus_id>')
def delete_bus(bus_id):
    if 'user_id' not in session:
        return redirect('/login')
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM buses WHERE id = %s AND user_id = %s", (bus_id, session['user_id']))
    db.commit()
    return redirect(url_for('admin.manage_buses'))


@admin_bp.route('/drivers')
def manage_drivers():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM drivers")
    drivers = cursor.fetchall()
    db.close()

    return render_template('drivers.html', drivers=drivers)

@admin_bp.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        license_number = request.form['license_number']
        phone_number = request.form['phone_number']

        db = db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO drivers (name, license_number, phone_number) VALUES (%s, %s, %s)",
                       (name, license_number, phone_number))
        db.commit()
        db.close()

        return redirect(url_for('admin.manage_drivers'))

    return render_template('add_driver.html')

@admin_bp.route('/delete_driver/<int:driver_id>')
def delete_driver(driver_id):
    if 'user_id' not in session:
        return redirect('/login')
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM drivers WHERE id = %s", (driver_id,))
    db.commit()
    return redirect(url_for('admin.manage_drivers'))
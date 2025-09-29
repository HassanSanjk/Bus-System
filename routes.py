from flask import Flask, render_template, request, redirect, session, Blueprint, url_for
from db import db_connection

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/routes')
def manage_routes():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM routes")
    routes = cursor.fetchall()
    db.close()

    return render_template('routes.html', routes=routes)

@routes_bp.route('/add_route', methods=['GET', 'POST'])
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

@routes_bp.route('/delete_route/<int:route_id>')
def delete_route(route_id):
    if 'user_id' not in session:
        return redirect('/login')
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM routes WHERE id = %s AND user_id = %s", (route_id, session['user_id']))
    db.commit()
    return redirect(url_for('routes.routes'))
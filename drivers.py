from flask import Blueprint, render_template, request, redirect, session
from db import db_connection

drivers_bp = Blueprint('drivers', __name__)

@drivers_bp.route('/drivers', methods = ['GET','POST'])
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

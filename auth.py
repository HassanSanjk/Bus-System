from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = db_connection()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        con.close()

        if user and check_password_hash(user['password'], password):
            session["user_id"] = user['id']
            return redirect(url_for("dashboard", name = user['name']))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("auth.login"))

    return render_template('login.html')


@auth_bp.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password1']
        phone = request.form['phone']
        hased_password = generate_password_hash(password,)

        con = db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        con.close()

        if user:
            flash("Email already exists", "danger")
            return redirect(url_for("auth.register"))

        con = db_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO users (name, email, password, phone, role) VALUES (%s, %s, %s, %s, 'user')", (name, email, hased_password, phone))
        con.commit()
        con.close()

        return redirect(url_for("login"))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

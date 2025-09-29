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
            session["name"] = user['name']
            if user['role'] == 'admin':
                return redirect(url_for("views.admin"))
            else:
                return redirect(url_for("views.dashboard"))
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
        password2 = request.form['password2']
        phone = request.form['phone']
        hashed_password = generate_password_hash(password)


        con = db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        con.close()

        print(user)

        if user:
            flash("Email already exists", category="error")
        elif len(email) <4:
            flash("Email must be greater than 3 characters", category="error")
        elif len(name) <2:
            flash("Name must be greater than 1 character", category="error")
        elif password != password2:
            flash("Passwords don't match", category="error")
        elif len(password) <8:
            flash("Password must be at least 8 characters", category="error")
        elif len(phone) <10:
            flash("Phone number must be at least 10 characters", category="error")
        else:
            con = db_connection()
            cursor = con.cursor()
            cursor.execute("INSERT INTO users (name, email, password, phone, role) VALUES (%s, %s, %s, %s, 'user')", (name, email, hashed_password, phone))
            con.commit()
            con.close()
            flash("Account created!", category="success")
            return redirect(url_for("auth.login"))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

from flask import Flask, render_template, redirect, session, Blueprint

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')


@views_bp.route('/dashboard/<name>')
def dashboard(name):
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html', name = name)

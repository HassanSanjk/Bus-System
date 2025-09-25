from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from db import db_connection

buses_bp = Blueprint('buses', __name__)

@buses_bp.route('/add_bus', methods = ['GET','POST'])
def add_bus():
    if 'user_id' not in session:
        return redirect('/login')

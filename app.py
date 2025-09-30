from flask import Flask, render_template, request, redirect, url_for, session, flash
from views import views_bp
from auth import auth_bp
from admin import admin_bp


app = Flask(__name__)
app.secret_key = "SECRET_KEY"

app.register_blueprint(views_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)


if __name__ == '__main__':
    app.run(debug = True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from views import views_bp
from auth import auth_bp
from bookings import bookings_bp
from buses import buses_bp
from routes import routes_bp
from drivers import drivers_bp


app = Flask(__name__)
app.secret_key = "SECRET_KEY"

app.register_blueprint(views_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(buses_bp)
app.register_blueprint(routes_bp)
app.register_blueprint(drivers_bp)


if __name__ == '__main__':
    app.run(debug = True)
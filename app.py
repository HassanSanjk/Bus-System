from flask import Flask, render_template, request, redirect, url_for
import mysql.connector



app = Flask(__name__)
app.secret_key = "SECRET_KEY"





if __name__ == '__main__':
    app.run(debug = True)
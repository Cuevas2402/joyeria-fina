from app import app #, mysql
from flask import render_template, request

@app.route('/')
def login():
    return render_template('login.html')

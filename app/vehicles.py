from app import app #, mysql
from flask import render_template, request, session, url_for, redirect

@app.route('/vehicles')
def show_vehicles():
    if 'username' in session:
        return render_template('vehicles.html')
    else:
        return redirect(url_for('login'))
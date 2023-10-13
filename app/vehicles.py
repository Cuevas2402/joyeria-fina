from app import app, mysql
from flask import render_template, request, session, url_for, redirect

@app.route('/vehicles')
def show_vehicles():
    if 'username' in session:

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT id, name FROM truck LIMIT 10;')

        vehicles = cursor.fetchall()
        return render_template('vehicles.html', vehicles=vehicles)
    else:
        return redirect(url_for('login'))
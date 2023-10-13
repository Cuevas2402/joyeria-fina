from app import app, mysql
from flask import render_template, request, session, url_for, redirect

@app.route('/branches')
def show_branches():
    if 'username' in session:
        
        cursor = mysql.connection.cursor()

        cursor.execute('SELECT id, name FROM company LIMIT 10;')

        branches = cursor.fetchall()
        
        return render_template('branches.html', branches = branches)
    else:
        return redirect(url_for('login'))

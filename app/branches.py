from app import app #, mysql
from flask import render_template, request, session, url_for, redirect

@app.route('/branches')
def show_branches():
    if 'username' in session:
        return render_template('branches.html')
    else:
        return redirect(url_for('login'))

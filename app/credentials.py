from app import app , mysql
from flask import render_template, request, session, url_for, redirect
import requests

app.secret_key = "nuestraClaveSecretaUWU"


@app.route('/')
def login():
    if 'type' not in session: 
        return render_template('login.html')
    else:
        if session['type'] == 1:
            return redirect(url_for('show_vehicles'))
        elif session['type'] == 2:
            return redirect(url_for('show_orders'))
        elif session['type'] == 3:
            return redirect(url_for('show_vehicles'))

@app.route('/logout')
def log_out():
    if 'username' in session:
        session.pop('username', None)

    if 'id' in session:
        session.pop('id', None)
    
    if 'admin' in session:
        session.pop('admin', None)
    
    if 'type' in session:
        session.pop('type', None)

        
    return redirect(url_for('login'))

@app.route('/iniciar_sesion', methods = ['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        if 'type' not in session:
            username = request.form.get('username') 
            password = request.form.get('password')

            datos = {'username': username, 'password' : password} 
            url = 'http://127.0.0.1:5000/authentication' 
            response = requests.post(url, data=datos)
            if response.status_code == 200:
                data = response.json()
                if data :
                    session['username'] = data['username']
                    session['admin'] = data['admin']
                    session['id'] = data['id']
                    session['type'] = data['type']

                    return redirect(url_for('login'))
                else:
                    return redirect(url_for('login'))
            else:
                
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/authentication', methods = ['GET', 'POST'])
def authentication():
    data = {}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM identity WHERE username = %s AND password = %s;"

        cursor.execute(sql, (username, password, ))

        results = cursor.fetchall()
        if len(results) > 0 :
            data = {}
            data['username'] = results[0][3]
            data['admin'] = results[0][5] == 1

            sql = "SELECT company_id FROM identity, identity_company WHERE identity.id = identity_company.identity_id AND identity.id = %s;"
            cursor.execute(sql, (results[0][0], ))

            results = cursor.fetchall()

            if(len(results) > 0):
                data['id'] = results[0][0]
                data['type'] = 1 
            else:
                data['id'] = None
                data['type'] = 2 if data['admin'] else 3

            cursor.close()
            return data
        else:
            return data 
    else:
        return data

        
            
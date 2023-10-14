from app import app #, mysql
from flask import render_template, request, session, url_for, redirect
import requests

app.secret_key = "nuestraClaveSecretaUWU"


@app.route('/')
def login():
    if 'username' not in session:
        return render_template('login.html')
    else:
        return redirect(url_for('show_vehicles'))

@app.route('/logout')
def log_out():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/iniciar_sesion', methods = ['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        if 'username' not in session:
            username = request.form.get('username') 
            password = request.form.get('password')
            
            #try:
                #response = requests.get(url)

                #if response.status_code == 200:
                    #data = response.json() 
                      
                #else:
                    #return "Error al recuperar los datos"

            #except requests.exceptions.RequestException as e:
                #return str(e), 500


            response = { 'usuario': username, 'admin': True, 'id' : 54}            
            session['username'] = response['usuario']
            session['admin'] = response['admin']
            session['id'] = response['id']

        return redirect(url_for('show_vehicles')) 


        
            
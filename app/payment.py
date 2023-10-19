from app import app , mysql
from flask import render_template, request, session, url_for, redirect
import requests

@app.route('/orders/asign/payment', methods=['GET', 'POST'])
def fetch_data_pago():
    if 'type' in session:
        if request.method == 'POST':
            
            return redirect(url_for('login'))

            id_branch = request.form.get('branch')
            id_company = request.form.get('company')
            id_vehicle = request.form.get('vehicle')
            app_url = "http://127.0.0.1:5000" #ip publica donde esté el servicio que manda datos
            response = requests.get(app_url)

            if response.status_code == 200:
                datos = response.json()
                return render_template('joyeria/paying.html', datos=datos)
            else:
                return redirect(url_for('login'))

        else:
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))
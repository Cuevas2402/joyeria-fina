from app import app , mysql
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, math

@app.route('/orders')
def show_orders():
    if 'type' in session:
        if session['type'] == 2:
            cursor = mysql.connection.cursor()

            cursor.execute('SELECT id, status FROM orders;')

            orders = cursor.fetchall()
            
            cursor.close()

            return render_template('joyeria/orders.html', orders = orders)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/orders/asign/<id>')
def show_asign_template(id):
    if 'type' in session:
        if session['type'] == 2:
            datos = {'id': id} 
            url = 'http://127.0.0.1:5000/get-branches' 
            response = requests.post(url, data=datos)
            
            if response.status_code == 200:
                orders = response.json()

                return render_template('joyeria/asign.html', orders = orders['nearest_branches'], label = 'order', id = id)

            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/get-branches', methods = ['GET', 'POST'])
def get_branches():
    if request.method == 'POST':
        order_id = request.form.get('id')

        cursor = mysql.connection.cursor()
        sql = "SELECT latitude, longitude FROM orders WHERE id = %s;"
        cursor.execute(sql, (order_id, ))
        order_coordinates = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        sql = "SELECT id, name, latitude, longitude FROM branch;"
        cursor.execute(sql)
        branches_coordinates = cursor.fetchall()
        cursor.close()
        distances = []

        x2, y2 = order_coordinates[0]
        for branch in branches_coordinates:
            branch_id, branch_name, x1, y1 = branch
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            distances.append((distance, branch_id, branch_name))
        
        distances.sort()
        shortest_distances = distances[:5]

        nearest_branches = [{'branch_id' : str(distance[1]), 'branch_name' : distance[2]} for distance in shortest_distances]

        return {'nearest_branches' : nearest_branches}

@app.route('/get-companies', methods = ['GET', 'POST'])
def get_companies():
    if request.method == 'POST':
        branch_id = request.form.get('id')

        cursor = mysql.connection.cursor()
        sql = "SELECT latitude, longitude FROM branch WHERE id = %s;"
        cursor.execute(sql, (branch_id, ))
        branch_coordinates = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        sql = "SELECT id, name, latitude, longitude FROM company;"
        cursor.execute(sql)
        companies_coordinates = cursor.fetchall()
        cursor.close()

        distances = []

        x2, y2 = branch_coordinates[0]
        for company in companies_coordinates:
            company_id, company_name, x1, y1 = company
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            distances.append((distance, company_id, company_name))
        
        distances.sort()
        shortest_distances = distances[:5]

        nearest_companies = [{'company_id' : str(distance[1]), 'company_name' : distance[2]} for distance in shortest_distances]

        return {'nearest_companies' : nearest_companies}

@app.route('/get-vehicles', methods = ['GET', 'POST'])
def get_vehicles():
    if request.method == 'POST':
        company_id = request.form.get('id')

        cursor = mysql.connection.cursor()
        sql = "SELECT id, name, fixed_price, km_fee FROM truck WHERE company_id = %s;"
        cursor.execute(sql, (company_id, ))
        vehicles = cursor.fetchall()
        cursor.close()

        return jsonify(vehicles)
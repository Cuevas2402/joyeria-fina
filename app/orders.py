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

@app.route('/orders/delete-order', methods = ['GET', 'POST'])
def delete_order():
    if 'type' in session and 'admin' in session:
        if session['type'] == 2 and session['admin']:
            if request.method == 'GET':

                id = request.args.get('id')

                cursor = mysql.connection.cursor()

                sql = "DELETE FROM order_detail WHERE order_id = %s"

                cursor.execute(sql, (id, ))

                sql = "DELETE FROM orders WHERE id = %s"

                cursor.execute(sql, (id, ))

                mysql.connection.commit()

                cursor.close()
            return redirect(url_for('show_orders'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/orders/details/<id>')
def details_order(id):
    if 'type' in session:
        if session['type'] == 2: 

            cursor = mysql.connection.cursor()

            sql = "SELECT COLUMN_NAME from information_schema.columns WHERE table_schema = 'integracion' AND table_name = 'orders';"

            cursor.execute(sql)

            atributos = cursor.fetchall()

            sql = "SELECT * FROM orders WHERE id = %s"

            cursor.execute(sql, (id, ))

            datos = cursor.fetchone()

            attr = []        
            for i in atributos:
                attr.append(i[0])
            
            results = {}
            
            for atributo, dato in zip(attr, datos):
                results[atributo] = dato
            
            cursor.close()

            return render_template('joyeria/details.html', results = results)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/orders/create')
def create_order_view():
    if 'type' in session:
        if session['type'] == 2:
            cursor = mysql.connection.cursor()
            
            cursor.execute("SELECT id FROM identity;")

            users = cursor.fetchall()

            cursor.close()

            return render_template('joyeria/create_order.html', users = users)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/create-order', methods = ['GET', 'POST'])
def create_order():
    if 'type' in session:
        if session['type'] == 3:
            if request.method == 'POST':
                cursor = mysql.connection.cursor()

                user_id = request.form.get('user_id')
                latitude = request.form.get('latitud') 
                longitude = request.form.get('longitud')
                productos = request.form.getlist('modelo')
                cantidades = request.form.getlist('cantidad')

                cursor.execute("INSERT INTO orders (identity_id, latitude, longitude, status) VALUES (%s, %s, %s, %s)", (user_id, latitude, longitude, 'Pending'))
                mysql.connection.commit()  

                cursor.execute("SELECT LAST_INSERT_ID()")
                pedido = cursor.fetchone()[0]
                c = {}
                for producto, cantidad in zip(productos, cantidades):
                    codigo = producto.split("|")
                    codigo = codigo[0].strip()
                    if codigo not in c:
                        cursor.execute("INSERT INTO order_detail (order_id, product_id, quantity) VALUES (%s, %s, %s)",(pedido, codigo, cantidad,))
                        c[codigo] = int(cantidad)
                    else:
                        c[codigo]+=int(cantidad)
                        cursor.execute("UPDATE order_detail SET quantity = %s WHERE order_id = %s AND product_id = %s", (c[codigo], pedido, pedido, ))
                    mysql.connection.commit()  

                cursor.close() 

                return redirect(url_for('show_orders')) 
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
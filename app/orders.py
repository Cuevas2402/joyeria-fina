from app import app , mysql
from flask import render_template, request, session, url_for, redirect
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

@app.route('/get-branches', methods = ['GET', 'POST'])
def get_branches():
    if request.method == 'POST':
        order_id = request.form.get('id')

        cursor = mysql.connection.cursor()
        sql = "SELECT latitude, longitude FROM order WHERE id = %s;"
        cursor.execute(sql, (order_id, ))
        order_coordinates = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        sql = "SELECT id, latitude, longitude FROM branch;"
        cursor.execute(sql)
        branches_coordinates = cursor.fetchall()
        cursor.close()

        distances = []

        x2, y2 = order_coordinates
        for branch in branches_coordinates:
            branch_id, x1, y1 = branch
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            distances.append((distance, branch_id))
        
        distances.sort()
        shortest_distances = distances[:5]

        nearest_branches = [distance[1] for distance in shortest_distances]

        return {'nearest_branches': nearest_branches}
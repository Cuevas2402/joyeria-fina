from app import app , mysql
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, math

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
        sql = "SELECT id, name, latitude, longitude FROM branch;"
        cursor.execute(sql)
        branches_coordinates = cursor.fetchall()
        cursor.close()

        distances = []

        x2, y2 = order_coordinates
        for branch in branches_coordinates:
            branch_id, x1, y1 = branch
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            distances.append((distance, branch_id, branch_name))
        
        distances.sort()
        shortest_distances = distances[:5]

        nearest_branches = [{'branch_id' : distance[1], 'branch_name' : distance[2]} for distance in shortest_distances]

        return {'nearest_branches' : nearest_branches}

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
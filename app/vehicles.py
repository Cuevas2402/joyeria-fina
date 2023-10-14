from app import app, mysql
from flask import render_template, request, session, url_for, redirect
from datetime import date

@app.route('/vehicles')
def show_vehicles():
    if 'id' in session:

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT id, name FROM truck WHERE company_id = %s LIMIT 10;', (session['id'], ))

        vehicles = cursor.fetchall()
        return render_template('company/vehicles.html', vehicles=vehicles)
    else:
        return redirect(url_for('login'))

@app.route('/vehicles/create')
def create_vehicle_view():
    
    if 'id' in session and session['admin']:
        return render_template('company/create_vehicle.html')
    else:
        return redirect(url_for('login'))

@app.route('/create-vehicle', methods = ['POST', 'GET'])
def create_vehicle():

    if 'id' in session and session['admin']:
        if request.method == 'POST':

            cursor = mysql.connection.cursor()

            name = request.form.get('name')
            company_id = request.form.get('company_id')
            total_distance = request.form.get('total_distance')
            route_count = request.form.get('route_count')
            average_duration = request.form.get('average_duration')
            average_speed = request.form.get('average_speed')
            average_stop_count_per_trip = request.form.get('average_stop_count_per_trip')
            average_distance_between_short_stops = request.form.get('average_distance_between_short_stops')
            average_stem_distance = request.form.get('average_stem_distance')
            average_trip_distance = request.form.get('average_trip_distance')
            short_stops_time = request.form.get('short_stops_time')
            traveling_time = request.form.get('traveling_time')
            resting_time = request.form.get('resting_time')
            stops_between_0_5 = request.form.get('stops_between_0_5')
            stops_between_5_15 = request.form.get('stops_between_5_15')
            stops_between_15_30 = request.form.get('stops_between_15_30')
            stops_between_30_60 = request.form.get('stops_between_30_60')
            stops_between_60_120 = request.form.get('stops_between_60_120')
            stops_between_120_plus = request.form.get('stops_between_120_plus')
            average_trip_stop_time = request.form.get('average_trip_stop_time')
            average_trip_traveling_time = request.form.get('average_trip_traveling_time')
            average_stop_count_per_trip_sd = request.form.get('average_stop_count_per_trip_sd')
            average_trip_distance_sd = request.form.get('average_trip_distance_sd')
            average_stem_distance_sd = request.form.get('average_stem_distance_sd')
            average_speed_sd = request.form.get('average_speed_sd')
            average_trip_duration_sd = request.form.get('average_trip_duration_sd')
            average_trip_stop_time_sd = request.form.get('average_trip_stop_time_sd')
            average_trip_traveling_time_sd = request.form.get('average_trip_traveling_time_sd')

            created_at = date.today()

            updated_at = date.today()

            aux1 = 0.0

            aux2 = 0.0

            aux3 = ""

            sql = "INSERT INTO truck (name, company_id, total_distance, route_count, average_duration, average_speed, average_stop_count_per_trip, average_distance_between_short_stops, average_stem_distance, average_trip_distance, short_stops_time, traveling_time, resting_time, stops_between_0_5, stops_between_5_15, stops_between_15_30, stops_between_30_60, stops_between_60_120, stops_between_120_plus, average_trip_stop_time, average_trip_traveling_time, average_stop_count_per_trip_sd, average_trip_distance_sd, average_stem_distance_sd, average_speed_sd, average_trip_duration_sd, average_trip_stop_time_sd, average_trip_traveling_time_sd, created_at, updated_at, aux1, aux2, aux3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            values = (name, company_id, total_distance, route_count, average_duration, average_speed, average_stop_count_per_trip, average_distance_between_short_stops, average_stem_distance, average_trip_distance, short_stops_time, traveling_time, resting_time, stops_between_0_5, stops_between_5_15, stops_between_15_30, stops_between_30_60, stops_between_60_120, stops_between_120_plus, average_trip_stop_time, average_trip_traveling_time, average_stop_count_per_trip_sd, average_trip_distance_sd, average_stem_distance_sd, average_speed_sd, average_trip_duration_sd, average_trip_stop_time_sd, average_trip_traveling_time_sd, created_at, updated_at, aux1, aux2, aux3)

            cursor.execute(sql, values)        

            mysql.connection.commit()

            cursor.close()

        return redirect(url_for('show_vehicles'))
    else:
        return redirect(url_for('login'))
    
@app.route('/vehicles/edit/<id>')
def edit_vehicle_show(id):

    if 'id' in session and session['admin']:
        if 'id' in session:
            cursor = mysql.connection.cursor()

            sql = "SELECT COLUMN_NAME from information_schema.columns WHERE table_schema = 'integracion' AND table_name = 'truck';"

            cursor.execute(sql)

            atributos = cursor.fetchall()

            cursor.close()

        return render_template('company/edit.html', atributos=atributos, id= id, label = 'vehicle')
    else:
        return redirect(url_for('login'))

@app.route('/edit-vehicle/<id>', methods = ['POST', 'GET'])
def  edit_vehicle(id):
    if 'id' in session and session['admin']:
        if request.method == 'POST':
            cursor = mysql.connection.cursor()

            atributo = request.form.get('atributo')

            valor = request.form.get('valor')

            sql = "UPDATE truck SET {} = '{}' WHERE id = {};".format(atributo, valor ,id, )

            cursor.execute(sql)

            mysql.connection.commit()

            cursor.close()

        return redirect(url_for('show_vehicles'))
    else:
        return redirect(url_for('login'))
            

@app.route('/vehicles/delete-vehicle', methods = ['GET', 'POST'])
def delete_vehicle():
    if 'id' in session and session['admin']:
        if request.method == 'GET':

            id = request.args.get('id')

            cursor = mysql.connection.cursor()

            sql = "DELETE FROM truck WHERE id = %s"

            cursor.execute(sql, (id, ))

            mysql.connection.commit()

        return redirect(url_for('show_vehicles'))
    else:
        return redirect(url_for('login'))

@app.route('/vehicles/detailes/<id>')
def details_vehicle(id):
    if 'id' in session:

        cursor = mysql.connection.cursor()

        sql = "SELECT COLUMN_NAME from information_schema.columns WHERE table_schema = 'integracion' AND table_name = 'truck';"

        cursor.execute(sql)

        atributos = cursor.fetchall()

        sql = "SELECT * FROM truck WHERE id = %s"

        cursor.execute(sql, (id, ))

        datos = cursor.fetchone()

        attr = []        
        for i in atributos:
            attr.append(i[0])
        
        results = {}
        
        for atributo, dato in zip(attr, datos):
            results[atributo] = dato

        return render_template('company/details.html', label = 'vehiculo', results = results)
    else:
        return redirect(url_for('login'))
    

    


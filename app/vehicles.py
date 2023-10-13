from app import app, mysql
from flask import render_template, request, session, url_for, redirect
from datetime import date

@app.route('/vehicles')
def show_vehicles():
    if 'username' in session:

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT id, name FROM truck LIMIT 10;')

        vehicles = cursor.fetchall()
        return render_template('vehicles.html', vehicles=vehicles)
    else:
        return redirect(url_for('login'))

@app.route('/vehicles/create')
def create_vehicle_view():
    if 'username' in session:
        
        return render_template('crud_vehicles/create.html')
    else:
        return redirect(url_for('login'))

@app.route('/create-vehicle', methods = ['POST', 'GET'])
def create_vehicle():
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


        return redirect(url_for('show_vehicles'))
    


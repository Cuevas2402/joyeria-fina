from app import app , mysql
from flask import render_template, request, session, url_for, redirect, jsonify

@app.route('/ordering')
def show_ordering():
    if 'type' in session:
        if session['type'] == 3:
            return render_template('user/ordering.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    
@app.route('/anillos')
def get_anillos():
    if 'type' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM products;')
        anillos = cursor.fetchall()
        cursor.close()
        return jsonify(anillos)
    else:
        return {}

@app.route('/register-order', methods = ['GET', 'POST'])
def register_order():
    if 'type' in session:
        if request.method == 'POST':
            cursor = mysql.connection.cursor()

            latitude = request.form.get('latitud') 
            longitude = request.form.get('longitud')
            productos = request.form.getlist('modelo')
            cantidades = request.form.getlist('cantidad')

            cursor.execute('SELECT id FROM identity WHERE username = %s LIMIT 1;', (session['username'], ))

            user_id = cursor.fetchall()

            cursor.execute("INSERT INTO orders (identity_id, latitude, longitude, status) VALUES (%s, %s, %s, %s)", (user_id[0][0], latitude, longitude, 'Pending'))
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

            return render_template('user/num_order.html', pedido=pedido)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

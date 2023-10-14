from app import app, mysql
from flask import render_template, request, session, url_for, redirect

@app.route('/branches')
def show_branches():
    if 'username' in session:
        
        cursor = mysql.connection.cursor()

        cursor.execute('SELECT id, name FROM company WHERE id = %s;', (session['id']))

        branches = cursor.fetchall()
        
        return render_template('branches.html', branches = branches)
    else:
        return redirect(url_for('login'))

@app.route('/branches/edit/<id>')
def edit_branches_show(id):

    if 'username' in session:
        cursor = mysql.connection.cursor()

        sql = "SELECT COLUMN_NAME from information_schema.columns WHERE table_schema = 'integracion' AND table_name = 'company';"

        cursor.execute(sql)

        atributos = cursor.fetchall()

        cursor.close()

        return render_template('edit.html', atributos=atributos, id= id, label = 'branch')

@app.route('/edit-branch/<id>', methods = ['POST', 'GET'])
def  edit_branch(id):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()

        atributo = request.form.get('atributo')

        valor = request.form.get('valor')

        sql = "UPDATE company SET {} = '{}' WHERE id = {};".format(atributo, valor ,id, )

        cursor.execute(sql)

        mysql.connection.commit()

        cursor.close()

        return redirect(url_for('show_branches'))

@app.route('/branches/delete-branch', methods = ['GET', 'POST'])
def delete_branch():

    if request.method == 'GET':

        id = request.args.get('id')

        cursor = mysql.connection.cursor()

        sql = "DELETE FROM company WHERE id = %s"

        cursor.execute(sql, (id, ))

        mysql.connection.commit()

    return redirect(url_for('show_branches'))

@app.route('/branches/detailes/<id>')
def details_branch(id):
    if 'username' in session:

        cursor = mysql.connection.cursor()

        sql = "SELECT COLUMN_NAME from information_schema.columns WHERE table_schema = 'integracion' AND table_name = 'company';"

        cursor.execute(sql)

        atributos = cursor.fetchall()

        sql = "SELECT * FROM company WHERE id = %s"

        cursor.execute(sql, (id, ))

        datos = cursor.fetchone()

        attr = []        
        for i in atributos:
            attr.append(i[0])
        
        results = {}
        
        for atributo, dato in zip(attr, datos):
            results[atributo] = dato

        return render_template('details.html', label = 'branch', results = results)

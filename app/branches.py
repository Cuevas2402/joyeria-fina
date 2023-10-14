from app import app, mysql
from flask import render_template, request, session, url_for, redirect

@app.route('/branches')
def show_branches():
    if 'type' in session:
        if session['type'] == 1:
            
            cursor = mysql.connection.cursor()

            cursor.execute('SELECT id, name FROM company WHERE id = %s;', (session['id'], ))

            branches = cursor.fetchall()

            cursor.close()
            
            return render_template('company/branches.html', branches = branches)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/branches/edit/<id>')
def edit_branches_show(id):
    if 'type' in session and 'admin' in session:
        if session['type'] == 1 and session['admin']:
            cursor = mysql.connection.cursor()

            sql = "SELECT COLUMN_NAME from information_schema.columns WHERE table_schema = 'integracion' AND table_name = 'company';"

            cursor.execute(sql)

            atributos = cursor.fetchall()

            cursor.close()

            return render_template('company/edit.html', atributos=atributos, id= id, label = 'branch')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/edit-branch/<id>', methods = ['POST', 'GET'])
def  edit_branch(id):
    if 'type' in session and 'admin' in session: 
        if session['type'] == 1 and session['admin']:

            if request.method == 'POST':
                cursor = mysql.connection.cursor()

                atributo = request.form.get('atributo')

                valor = request.form.get('valor')

                sql = "UPDATE company SET {} = '{}' WHERE id = {};".format(atributo, valor ,id, )

                cursor.execute(sql)

                mysql.connection.commit()

                cursor.close()

            return redirect(url_for('show_branches'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/branches/delete-branch', methods = ['GET', 'POST'])
def delete_branch():
    if 'type' in session and 'admin' in session:
        if session['type'] == 1 and session['admin']:
            if request.method == 'GET':

                id = request.args.get('id')

                cursor = mysql.connection.cursor()

                sql = "DELETE FROM company WHERE id = %s"

                cursor.execute(sql, (id, ))

                mysql.connection.commit()

                cursor.close()

            return redirect(url_for('show_branches'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/branches/details/<id>')
def details_branch(id):
    if 'type' in session:
        if session['type'] == 1: 

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
            
            cursor.close()

            return render_template('company/details.html', label = 'branch', results = results)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

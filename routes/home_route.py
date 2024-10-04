from routes import app, mysql
from flask import render_template, request, session


@app.route('/user')
def user_list():
    return render_template('user/list.html')

@app.route('/setting')
def setting():
    cursor = mysql.connection.cursor()
    if 'username' in session:
        cursor.execute("SELECT id, name, username, jurisdiction, phone FROM user WHERE username = %s", (session['username'],))
        data = cursor.fetchall()

        column_names = ['id', 'name', 'username', 'jurisdiction', 'phone']
        data_list = [dict(zip(column_names, row)) for row in data]

        cursor.close()
        return render_template('user/setting.html', data=data_list)
    else:
        return render_template('login.html')

@app.route('/host')
def host():
    return render_template('host.html')

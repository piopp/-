from routes import app, mysql
from flask import session, render_template, request

@app.route('/')
def login():
    return render_template('login.html')

@app.post('/api/login')
def login_with_id():
    js = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user where name = %s and password = %s", (js['username'], js['password'],))
    data = cursor.fetchall()
    cursor.close()
    if data:
        session['username'] = js['username']
        session['jurisdiction'] = str(data[0][4])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT login_permission FROM role where id = %s", (session['jurisdiction']))
        flag = cursor.fetchall()
        cursor.close()
        if flag[0][0] == 1:
            return {
                'code':0,
                'message':'登录成功'
            }
        else:
            return {
                'code':-1,
                'message':'无登录权限'
            }
    else:
        return {
            'code':-1,
            'message':'登录失败'
        }


@app.route('/home')
def tohome():
    username = session.get('username', 'Guest')
    if username != 'Guest':
        return render_template('home.html', username=username)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('jurisdiction', None)
    session.pop('username', None)
    # session.clear()
    return render_template('login.html')
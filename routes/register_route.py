from routes import app, mysql
from flask import render_template, request

@app.route('/register')
def register():
    return render_template('register.html')


@app.post('/api/register')
def register_with_id():
    js = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user where name = %s", (js['username'],))
    data = cursor.fetchall()
    if data:
        return {
            'code':-1,
            'message':'重复的用户名'
        }
    cursor.execute("SELECT * FROM user where phone = %s", (js['cellphone'],))
    data = cursor.fetchall()
    if data:
        return {
            'code':-1,
            'message':'手机号已被注册'
        }
    cursor.execute("INSERT INTO user (name,password,username,phone) VALUES (%s,%s,%s,%s)", (js['username'], js['password'], js['nickname'], js['cellphone'],))
    mysql.connection.commit()
    cursor.close()

    return {
        'code':0,
        'message':'注册成功'
    }

@app.route('/login')
def to_login():
    return render_template('login.html')
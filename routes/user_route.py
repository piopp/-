from routes import app, mysql
from flask import render_template, request, jsonify, session


@app.route('/user/list')
def userlist():
    return render_template("user/list.html")

@app.route('/user/edit', methods=['POST'])
def useredit():
    data = request.get_json()
    return render_template("user/edit.html", data = data)

@app.route('/user/add', methods=['POST'])
def useradd():
    data = request.get_json()
    return render_template("user/add.html", data = data)

@app.route('/user/save', methods=['POST'])
def usersave():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.form
    name = data.get('name')
    username = data.get('username')
    jurisdiction = int(data.get('jurisdiction'))
    phone = data.get('phone')
    password = data.get('password')
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO user  (name, username,password, jurisdiction, phone)  VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(sql, (name, username, password,jurisdiction, phone))
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '添加失败'})

@app.route('/user/delete', methods=['POST'])
def userdelete():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.get_json()
    ids = [item["id"] for item in data]
    cursor = mysql.connection.cursor()
    placeholders = ','.join(['%s'] * len(ids))
    sql = "DELETE FROM user WHERE id IN ({})".format(placeholders)
    cursor.execute(sql, ids)
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1, 'message': '删除成功'})
    else:
        return jsonify({'success': 0, 'message': '添加失败'})


@app.route('/user/save1', methods=['POST'])
def usersave1():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.form
    user_id = int(data.get('id'))
    name = data.get('name')
    username = data.get('username')
    jurisdiction = int(data.get('jurisdiction'))
    phone = data.get('phone')
    cursor = mysql.connection.cursor()
    sql = "UPDATE user SET name = %s, username = %s, jurisdiction = %s,phone = %s WHERE id = %s"
    cursor.execute(sql, (name, username, jurisdiction, phone, user_id))
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '未修改内容'})


@app.route('/getuser')
def getuser():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    cursor = mysql.connection.cursor()

    sql = "SELECT id, name, username, jurisdiction, phone FROM user LIMIT %s OFFSET %s"
    cursor.execute(sql, (limit, offset))
    result = cursor.fetchall()
    keys = ["id", "name", "username", "jurisdiction", "phone"]
    data = [dict(zip(keys, item)) for item in result]
    sql = "SELECT COUNT(*) FROM user"
    cursor.execute(sql)
    count = cursor.fetchall()
    cursor.close()

    # 返回JSON格式的数据给前端
    return jsonify({
        'code': 0,  # Layui表格默认要求的返回码
        'msg': '',
        'count': count,
        'data': data
    })

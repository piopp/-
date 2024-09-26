from routes import app, mysql
from flask import render_template, request, jsonify, session


@app.route('/role/list')
def rolelist():
    return render_template("role/list.html")

@app.route('/getrole')
def getrole():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM role LIMIT %s OFFSET %s"
    cursor.execute(sql, (limit, offset))
    result = cursor.fetchall()
    keys = ["id", "name", "login_permission", "user_permission", "role_permission", "sample_permission", "predictive_permission"]
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




@app.route('/role/edit', methods=['POST'])
def roleedit():
    data = request.get_json()
    return render_template("role/edit.html", data = data)

@app.route('/role/add', methods=['POST'])
def roleadd():
    data = request.get_json()
    return render_template("role/add.html", data = data)

@app.route('/role/save', methods=['POST'])
def rolesave():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT role_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.form
    id = data['id']
    name = data['name']
    login_permission = data['login_permission']
    user_permission = data['user_permission']
    role_permission = data['role_permission']
    sample_permission = data['sample_permission']
    predictive_permission = data['predictive_permission']
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO role  (name, login_permission, user_permission, role_permission, sample_permission, predictive_permission)  VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (name, login_permission, user_permission, role_permission, sample_permission, predictive_permission))
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '添加失败'})

@app.route('/role/delete', methods=['POST'])
def roledelete():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT role_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.get_json()
    ids = [item["id"] for item in data]
    cursor = mysql.connection.cursor()
    placeholders = ','.join(['%s'] * len(ids))  # 创建与 ids 列表长度相同的占位符字符串
    sql = "DELETE FROM role WHERE id IN ({})".format(placeholders)
    cursor.execute(sql, ids)
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '添加失败'})


@app.route('/role/save1', methods=['POST'])
def rolesave1():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT role_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.form
    id = data['id']
    name = data['name']
    login_permission = data['login_permission']
    user_permission = data['user_permission']
    role_permission = data['role_permission']
    sample_permission = data['sample_permission']
    predictive_permission = data['predictive_permission']
    cursor = mysql.connection.cursor()
    sql = "UPDATE role SET name = %s, login_permission = %s, user_permission = %s,role_permission = %s,sample_permission = %s,predictive_permission = %s WHERE id = %s"
    cursor.execute(sql, (name, login_permission, user_permission, role_permission, sample_permission, predictive_permission,id))
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '未修改内容'})
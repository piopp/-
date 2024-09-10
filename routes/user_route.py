from routes import app, mysql
from flask import render_template, request, jsonify

@app.route('/user/list')
def userlist():
    return render_template("user/list.html")

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

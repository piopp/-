from routes import app, mysql
from flask import render_template, request, jsonify

@app.route('/patient/list')
def patientlist():
    return render_template("patient/list.html")

@app.route('/getpatient')
def getpatient():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM patient LIMIT %s OFFSET %s"
    cursor.execute(sql, (limit, offset))
    result = cursor.fetchall()
    keys = ["pid", "pname", "psex", "pphone", "padd", "phistory", "createtime"]
    data = [dict(zip(keys, item)) for item in result]
    sql = "SELECT COUNT(*) FROM patient"
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

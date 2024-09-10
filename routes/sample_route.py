from routes import app, mysql
from flask import render_template, request, jsonify

@app.route('/sample/list')
def samplelist():
    return render_template("sample/list.html")

@app.route('/getsample')
def getsample():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM sample LIMIT %s OFFSET %s"
    cursor.execute(sql, (limit, offset))
    result = cursor.fetchall()
    keys = ["id", "透析方式", "透析年限", "透析通路", "平时脱水量比例","充血性心衰","透析时血压","血红蛋白","钙","白蛋白","前白蛋白","LDH","铁","铁蛋白","住院"]
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

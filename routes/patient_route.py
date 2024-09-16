import datetime

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



@app.route('/patient/edit', methods=['POST'])
def patientedit():
    data = request.get_json()
    return render_template("patient/edit.html", data = data)

@app.route('/patient/add', methods=['POST'])
def patientadd():
    data = request.get_json()
    return render_template("patient/add.html", data = data)

@app.route('/patient/save', methods=['POST'])
def patientsave():
    data = request.form
    pname = data['pname']
    phistory = data['phistory']
    psex= data['psex']
    pphone = data['pphone']
    padd = data['padd']
    cursor = mysql.connection.cursor()
    createtime = datetime.datetime.now()
    sql = "INSERT INTO patient  (pname, psex, pphone, padd, phistory, createtime)  VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (pname, psex, pphone, padd, phistory, createtime))
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '添加失败'})

@app.route('/patient/delete', methods=['POST'])
def patientdelete():
    data = request.get_json()
    ids = [item["pid"] for item in data]
    cursor = mysql.connection.cursor()
    placeholders = ','.join(['%s'] * len(ids))  # 创建与 ids 列表长度相同的占位符字符串
    sql = "DELETE FROM patient WHERE pid IN ({})".format(placeholders)
    cursor.execute(sql, ids)
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '添加失败'})


@app.route('/patient/save1', methods=['POST'])
def patientsave1():
    data = request.form
    pid = data['pid']
    pname = data['pname']
    phistory = data['phistory']
    psex= data['psex']
    pphone = data['pphone']
    padd = data['padd']
    createtime = datetime.datetime.now()
    cursor = mysql.connection.cursor()
    sql = "UPDATE patient SET pname = %s, psex = %s, pphone = %s,padd = %s,phistory = %s,createtime = %s WHERE pid = %s"
    cursor.execute(sql, (pname, psex, pphone, padd, phistory, createtime, pid))
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '未修改内容'})
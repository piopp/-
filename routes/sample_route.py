from routes import app, mysql
from flask import render_template, request, jsonify, session


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
    sql = "SELECT COUNT(*) FROM sample"
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


@app.route('/sample/edit', methods=['POST'])
def sampleedit():
    data = request.get_json()
    return render_template("sample/edit.html", data = data)

@app.route('/sample/add', methods=['POST'])
def sampleadd():
    data = request.get_json()
    return render_template("sample/add.html", data = data)

@app.route('/sample/save', methods=['POST'])
def samplesave():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT sample_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.form
    id = data['id']
    透析方式 = data['透析方式']
    透析通路 = data['透析通路']
    平时脱水量比例 = data['平时脱水量比例']
    充血性心衰 = data['充血性心衰']
    透析时血压 = data['透析时血压']
    血红蛋白 = data['血红蛋白']
    钙 = data['钙']
    白蛋白 = data['白蛋白']
    前白蛋白 = data['前白蛋白']
    LDH = data['LDH']
    铁 = data['铁']
    铁蛋白 = data['铁蛋白']
    住院 = data['住院']
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO sample  (透析方式, 透析通路, 平时脱水量比例, 充血性心衰, 透析时血压, 血红蛋白, 钙, 白蛋白, 前白蛋白, LDH, 铁, 铁蛋白, 住院)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (透析方式, 透析通路, 平时脱水量比例, 充血性心衰, 透析时血压, 血红蛋白, 钙, 白蛋白, 前白蛋白, LDH, 铁, 铁蛋白, 住院))
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '添加失败'})

@app.route('/sample/delete', methods=['POST'])
def sampledelete():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT sample_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.get_json()
    ids = [item["id"] for item in data]
    cursor = mysql.connection.cursor()
    placeholders = ','.join(['%s'] * len(ids))  # 创建与 ids 列表长度相同的占位符字符串
    sql = "DELETE FROM sample WHERE id IN ({})".format(placeholders)
    cursor.execute(sql, ids)
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '添加失败'})


@app.route('/sample/save1', methods=['POST'])
def samplesave1():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT sample_permission FROM role where id = %s", (session['jurisdiction']))
    flag = cursor.fetchall()
    cursor.close()
    if flag[0][0] == 0:
        return jsonify({'success': 0, 'message': '无权限'})
    data = request.form
    id = data['id']
    透析方式 = data['透析方式']
    透析通路 = data['透析通路']
    平时脱水量比例 = data['平时脱水量比例']
    充血性心衰 = data['充血性心衰']
    透析时血压 = data['透析时血压']
    血红蛋白 = data['血红蛋白']
    钙 = data['钙']
    白蛋白 = data['白蛋白']
    前白蛋白 = data['前白蛋白']
    LDH = data['LDH']
    铁 = data['铁']
    铁蛋白 = data['铁蛋白']
    住院 = data['住院']
    cursor = mysql.connection.cursor()
    sql = "UPDATE sample SET 透析方式 = %s, 透析通路 = %s, 平时脱水量比例 = %s,充血性心衰 = %s,透析时血压 = %s,血红蛋白 = %s,钙 = %s,白蛋白 = %s,前白蛋白 = %s,LDH = %s,铁 = %s,铁蛋白 = %s,住院 = %s WHERE id = %s"
    cursor.execute(sql, (透析方式, 透析通路, 平时脱水量比例, 充血性心衰, 透析时血压, 血红蛋白, 钙, 白蛋白, 前白蛋白, LDH, 铁, 铁蛋白, 住院,id))
    mysql.connection.commit()
    cursor.close()
    if cursor.rowcount > 0:
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0, 'message': '未修改内容'})
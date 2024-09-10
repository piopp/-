from routes import app, mysql
from flask import render_template, request

@app.route('/user')
def user_list():
    return render_template('user/list.html')

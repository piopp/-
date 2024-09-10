from routes import app, mysql
from flask import render_template, request, jsonify

@app.route('/predict/list')
def predictlist():
    return render_template("predict/list.html")

import numpy as np

from routes import app, mysql
from flask import render_template, request, jsonify
from joblib import dump, load

@app.route('/predict/list')
def predictlist():
    return render_template("predict/list.html")


@app.route('/predict/save', methods=['POST'])
def predict():
    form_data = request.form
    X_new = [float(form_data.get(key)) for key in form_data if key != 'id']

    X_new = np.array([X_new])
    clf = load('predict.joblib')

    predictions = clf.predict(X_new)

    return jsonify({'success': 1, 'message': predictions.tolist()})
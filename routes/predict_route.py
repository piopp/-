from routes import app, mysql
from flask import render_template, request, jsonify
from joblib import dump, load

@app.route('/predict/list')
def predictlist():
    return render_template("predict/list.html")


@app.route('/predict/predict', methods=['POST'])
def predict():
    X_new = request.get_json(force=True)

    clf = load('svm_model.joblib')

    predictions = clf.predict(X_new)

    print(predictions)
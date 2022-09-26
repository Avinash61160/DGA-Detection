import catboost

import joblib

from flask import Flask,request,app,jsonify,url_for,render_template

import numpy as np
import pandas as pd

app = Flask(__name__)

cat_model = joblib.load("catboost.joblib")


@app.route('/')

def home():

    return render_template('home.html')


@app.route('/predict_api',methods=['POST'])


def predict_api():

    data=request.json['data']
    print(data)

    print(np.array(list(data.values())).reshape(1,-1))

    new_data=sc.transform(np.array(list(data.values())).reshape(1,-1))

    output= cat_model.predict(new_data)

    print(output[0])

    return jsonify(output[0])

@app.route('/predict',methods=['POST'])

def predict():
    data=[float(x) for x in request.form.values()]
    final_input = sc.transform(np.array(data).reshape(1,-1))
    print(final_input)
    return render_template("home.html",pred_text=cat_model.predict(final_input)[0])

@app.route('/pred',methods=['POST'])


def pred():
    data=[float(x) for x in request.form.values()]
    final_input = sc.transform(np.array(data).reshape(1,-1))
    print(final_input)
    out = cat_model.predict(final_input)[0]
    return render_template("home.html",pred_text=out)

if __name__=="__main__":
    app.run(debug=True)
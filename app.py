#pip install catboost
import catboost
import joblib
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app = Flask(__name__)
cat_model = joblib.load("catboost.joblib")
scale = joblib.load("sc.joblib")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])

def predict():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=sc.transform(np.array(list(data.values())).reshape(1,-1))
    output= cat_model.predict(new_data)
    print(output[0])
    return jsonify(output[0])


if __name__=="__main__":
    app.run(debug=True)
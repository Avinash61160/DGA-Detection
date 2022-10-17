import catboost

import joblib
import re
from scipy import stats

from flask import Flask,request,app,jsonify,url_for,render_template

import numpy as np
import pandas as pd

# init app
app = Flask(__name__)

# model
cat_model = joblib.load("catboost.joblib")


@app.route('/',methods=['GET'])

def home():

    return render_template('home.html')

@app.route('/predict',methods=['GET','POST'])

def work():
    str = request.form.get("Domain_Name")

    op = []
    op.append(len(str))                          # For length of string
        
    num = "".join(re.findall("[0-9]+",str))
    if num.isnumeric():
        op.append(1)
    else:
        op.append(0)                         # Domain names with only digits   
            
    vowels = 0
    consonant = 0
    specialChar = 0
    digit = 0
  
    for i in range(0, len(str)): 
          
        ch = str[i] 
  
        if ( (ch >= 'a' and ch <= 'z') or 
             (ch >= 'A' and ch <= 'Z') ): 
  
            ch = ch.lower()
  
            if (ch == 'a' or ch == 'e' or ch == 'i' 
                        or ch == 'o' or ch == 'u'):
                vowels += 1
            else:
                consonant += 1
          
        elif (ch >= '0' and ch <= '9'):
            digit += 1
        else:
            specialChar += 1
    
    try:
        ratio = (vowels / (vowels + consonant)) * 100
        
    except:
        if((vowels + consonant) <= 0) :
            ratio = 0
    op.append(ratio)                         # To find vowel to consonent ratio 
    
    
    if str.isalpha():
        if len(str)==1:
            op.append(ord(str))
        else:
            op.append(1)
    else:
        op.append(0)                        # Domain name with only one char
            
            
    isNum = 0
    for i in range(0, len(str)):
        
        ch = str[i]
        
        if (ch >= '0' and ch <= '9'):
            isNum += 1
        else:
            pass
    op.append(isNum)                       # Number of digits in domain name
    
    word = "".join(re.findall("[a-zA-Z]+",str))
    word.lower()
    cmp = "aeiou"
    m_val = 0
    t_tal = 0
    for i in range(len(str)):
        if str[i] in cmp:
            t_tal += 1
        elif str[i] not in cmp:
            if m_val < t_tal:
                m_val = t_tal
                t_tal = 0
        if i == len(str) - 1 :
            if m_val < t_tal:
                m_val = t_tal
    op.append(m_val)                      # Max consicutive vowels 
    
    word = "".join(re.findall("[a-zA-Z]+",str))
    word.lower()
    cmp = "bcdfghjklmnpqrstvwxyz"
    m_val = 0
    t_tal = 0
    for i in range(len(str)):
        if str[i] in cmp:
            t_tal += 1
        elif str[i] not in cmp:
            if m_val < t_tal:
                m_val = t_tal
                t_tal = 0
        if i == len(str) - 1 :
            if m_val < t_tal:
                m_val = t_tal
    op.append(m_val)

    opp = stats.zscore(op)

    prediction = cat_model.predict(opp)

    if prediction == 0:
        
        return render_template("home.html",prediction_text = "Domain Name Is Algorithmically Generated")

    else:

        
        return render_template("home.html",prediction_text = "Domain Name Is LEGIT")

if __name__=="__main__":
    app.run(debug=True)
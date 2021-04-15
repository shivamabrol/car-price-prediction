from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 0
        Fuel_Type_Electric = 0
        Fuel_Type_LPG = 0
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
        if(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Diesel=1
        if(Fuel_Type_Petrol=='Electric'):
                Fuel_Type_Electric=1
        if(Fuel_Type_Petrol=='LPG'):
            Fuel_Type_LPG=1

        Year=2021-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        Seller_Type_Individual= 0
        Seller_Type_Trustmark = 0
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        if(Seller_Type_Individual=='Trustmark'):
            Seller_Type_Trustmark=1

        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        fourth_owner = 0
        second_owner = 0
        third_owner = 0
        Owner=int(request.form['Owner'])
        if(Owner == 2):
            second_owner = 1
        if(Owner == 3):
            third_owner = 1
        if(Owner == 4):
            fourth_owner = 1
        

        prediction=model.predict([[Kms_Driven2,Year,Fuel_Type_Diesel,Fuel_Type_Electric, Fuel_Type_LPG,Fuel_Type_Petrol,
                                   Seller_Type_Individual,0,Transmission_Mannual, fourth_owner, second_owner, 0, third_owner]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)

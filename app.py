import pickle
from flask import Flask, request, jsonify, url_for, render_template
from flask_cors import CORS

import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the model and scaler
model = pickle.load(open('regmodel.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        # Get the input JSON
        input_json = request.get_json()

        # Extract the 'data' dictionary
        data = input_json['data']

        # Create a DataFrame with the right column names
        new_data = pd.DataFrame([data])  # <-- VERY IMPORTANT (list of dict)

        # Predict
        prediction = model.predict(new_data)

        # Send the prediction
        return jsonify({'prediction': prediction[0]})
    
    except Exception as e:
        # If any error, show it nicely
        return jsonify({'error': str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the form
        data = [float(x) for x in request.form.values()]
        
        # Convert to a DataFrame because your model expects column names
        columns = ['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','B','LSTAT']
        input_data = pd.DataFrame([data], columns=columns)
        
        # Make prediction
        prediction = model.predict(input_data)[0]

        return render_template('home.html', prediction_text=f"The House Price Prediction is: ${prediction:.2f}")
    
    except Exception as e:
        return render_template('home.html', prediction_text=f"Error: {str(e)}")
    
    
if __name__ == '__main__':
    app.run(debug=True)
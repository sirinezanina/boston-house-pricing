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

@app.route('/predict', methods=['POST'])
def predict():
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

if __name__ == '__main__':
    app.run(debug=True)
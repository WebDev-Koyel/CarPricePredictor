from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load the pre-trained model and preprocessor
try:
    model = pickle.load(open('best_model.pkl', 'rb'))
    # preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))
except FileNotFoundError as e:
    print(f"Error: {e}")
    model, preprocessor = None, None

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not preprocessor:
        return jsonify({'error': 'Model or preprocessor not found'}), 500

    try:
        data = request.json
        attributes = [
            'Owner_Type', 'Mileage', 'Engine', 'Power', 'Seats',
            'New_Price', 'depreciation_rate', 'car_age'
        ]
        
        # Extract values in the correct order
        values = [data[attr] for attr in attributes]

        # Convert to numpy array and reshape
        processed_data = preprocessor.transform([values])  
        prediction = model.predict(processed_data)[0]

        return jsonify({'predicted_price': round(prediction, 2)})

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)

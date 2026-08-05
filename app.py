from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import os
from datetime import datetime

app = Flask(__name__)

# Load model pipeline securely
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'pipeline.pkl')
try:
    with open(MODEL_PATH, 'rb') as f:
        model_pipeline = pickle.load(f)
except Exception as e:
    model_pipeline = None
    print(f"Error loading model pipeline: {e}")

def validate_and_parse_input(data):
    """Validates and parses car parameters from form or JSON payload."""
    current_year = datetime.now().year
    
    try:
        year = int(data.get('year', 0))
        if year < 1990 or year > current_year:
            return None, f"Year must be between 1990 and {current_year}."
        
        km_driven = int(data.get('kilometers_driven', -1))
        if km_driven < 0 or km_driven > 1_000_000:
            return None, "Kilometers driven must be between 0 and 1,000,000 km."
            
        fuel_type = str(data.get('fuel_type', '')).strip()
        if fuel_type not in ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric']:
            return None, "Invalid fuel type selected."
            
        transmission = str(data.get('transmission', '')).strip()
        if transmission not in ['Manual', 'Automatic']:
            return None, "Invalid transmission selected."
            
        owner_type = str(data.get('owner_type', '')).strip()
        if owner_type not in ['First', 'Second', 'Third', 'Fourth & Above']:
            return None, "Invalid owner type selected."
            
        seats = float(data.get('seats', 0))
        if seats < 2 or seats > 10:
            return None, "Seats must be between 2 and 10."
            
        mileage = float(data.get('mileage', 0))
        if mileage <= 0 or mileage > 50:
            return None, "Mileage must be between 0.1 and 50 kmpl."
            
        engine = int(data.get('engine', 0))
        if engine < 500 or engine > 8000:
            return None, "Engine capacity must be between 500 CC and 8000 CC."
            
        power = float(data.get('power', 0))
        if power < 20 or power > 1000:
            return None, "Power must be between 20 bhp and 1000 bhp."
            
        parsed_data = {
            'Year': year,
            'Kilometers_Driven': km_driven,
            'Fuel_Type': fuel_type,
            'Transmission': transmission,
            'Owner_Type': owner_type,
            'Seats': seats,
            'Mileage': mileage,
            'Engine': engine,
            'Power': power
        }
        return parsed_data, None
    except (ValueError, TypeError) as err:
        return None, f"Invalid input format: {str(err)}"

def predict_car_price(parsed_data):
    if model_pipeline is None:
        raise ValueError("Model pipeline is not loaded.")
    input_df = pd.DataFrame([parsed_data])
    prediction = model_pipeline.predict(input_df)
    return max(0.1, float(prediction[0]))

def format_inr(lakh_value):
    """Convert Lakh value to human readable INR string (e.g., 5.45 -> ₹ 5.45 Lakh / ₹ 5,45,000)."""
    rupees = int(round(lakh_value * 100000))
    formatted_rupees = f"₹ {rupees:,}"
    return f"₹ {lakh_value:.2f} Lakh ({formatted_rupees})"

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_price = None
    formatted_price = None
    error_message = None
    input_values = {}

    if request.method == 'POST':
        input_values = request.form.to_dict()
        parsed_data, error = validate_and_parse_input(request.form)
        if error:
            error_message = error
        else:
            try:
                raw_price = predict_car_price(parsed_data)
                predicted_price = round(raw_price, 2)
                formatted_price = format_inr(predicted_price)
            except Exception as e:
                error_message = f"Prediction error: {str(e)}"

    return render_template(
        'index.html',
        predicted_price=predicted_price,
        formatted_price=formatted_price,
        error_message=error_message,
        input_values=input_values,
        current_year=datetime.now().year
    )

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Request payload must be JSON.'}), 400
    
    data = request.get_json()
    parsed_data, error = validate_and_parse_input(data)
    if error:
        return jsonify({'success': False, 'error': error}), 400
        
    try:
        raw_price = predict_car_price(parsed_data)
        predicted_lakh = round(raw_price, 2)
        return jsonify({
            'success': True,
            'predicted_price_lakh': predicted_lakh,
            'formatted_price': format_inr(predicted_lakh),
            'inputs': parsed_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
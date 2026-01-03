#!/usr/bin/env python3
"""
AQI Prediction Testing Script
Test single records from CSV files using the trained regression model.
"""

import pandas as pd
import joblib
import os

def load_model_and_scaler():
    """Load the trained model and scaler."""
    try:
        model = joblib.load('rf_reg_model.pkl')
        scaler = joblib.load('scaler_reg.pkl')
        print("✓ Model and scaler loaded successfully")
        return model, scaler
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("Make sure rf_reg_model.pkl and scaler_reg.pkl exist in the current directory")
        return None, None

def predict_aqi_from_csv(csv_file_path, model, scaler):
    """
    Load a single record from CSV and predict AQI.

    Parameters:
    csv_file_path (str): Path to the CSV file containing pollutant data
    model: Trained regression model
    scaler: Fitted scaler

    Returns:
    dict: Dictionary containing predictions and pollutant values
    """
    try:
        # Check if file exists
        if not os.path.exists(csv_file_path):
            return {"error": f"File {csv_file_path} not found"}

        # Load the CSV file
        test_df = pd.read_csv(csv_file_path)

        if len(test_df) == 0:
            return {"error": "CSV file is empty"}

        # Take the first record
        sample = test_df.iloc[0].to_dict()

        # Required features in correct order
        required_features = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']

        # Prepare input data
        input_data = [[sample.get(feature, 0) for feature in required_features]]
        input_df = pd.DataFrame(input_data, columns=required_features)

        # Scale the input
        scaled_input = scaler.transform(input_df)

        # Make prediction
        predicted_aqi = model.predict(scaled_input)[0]

        # Return results
        result = {
            'predicted_aqi': round(predicted_aqi, 2),
            'pollutant_values': sample,
            'csv_file': csv_file_path,
            'status': 'success'
        }

        return result

    except Exception as e:
        return {"error": f"Error processing {csv_file_path}: {str(e)}"}

def main():
    """Main function to test all single-record files."""
    print("AQI Prediction Testing Script")
    print("=" * 40)

    # Load model and scaler
    model, scaler = load_model_and_scaler()
    if model is None or scaler is None:
        return

    # Test files for each category
    test_files = {
        'Good': 'good_single.csv',
        'Satisfactory': 'satisfactory_single.csv',
        'Moderate': 'moderate_single.csv',
        'Poor': 'poor_single.csv',
        'Very Poor': 'very_poor_single.csv',
        'Severe': 'severe_single.csv'
    }

    print("\nTesting single records from each AQI category:")
    print("-" * 50)

    for category, filename in test_files.items():
        result = predict_aqi_from_csv(filename, model, scaler)

        if 'error' in result:
            print(f"✗ {category}: {result['error']}")
        else:
            print(f"✓ {category}:")
            print(f"  Predicted AQI: {result['predicted_aqi']:.2f}")
            pollutants = result['pollutant_values']
            print(f"  Key pollutants: PM2.5={pollutants['PM2.5']:.1f}, PM10={pollutants['PM10']:.1f}")
            print(f"                   NO2={pollutants['NO2']:.2f}, SO2={pollutants['SO2']:.2f}")
            print(f"                   CO={pollutants['CO']:.2f}, O3={pollutants['O3']:.2f}")
        print()

    print("Testing completed!")

if __name__ == "__main__":
    main()
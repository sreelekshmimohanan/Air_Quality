#!/usr/bin/env python3
"""
Debug script for CSV upload and form filling issue
"""

import os
import sys
import django
import csv
import io

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_quality.settings')

django.setup()

def debug_csv_upload():
    """Debug the CSV upload and form filling process"""
    print("Debugging CSV Upload and Form Filling")
    print("=" * 50)

    # Test 1: Check if poor_single.csv exists and can be read
    csv_path = os.path.join(os.path.dirname(__file__), 'ML', 'poor_single.csv')
    print("1. Checking CSV file...")

    if not os.path.exists(csv_path):
        print("   ❌ poor_single.csv not found!")
        return False

    print("   ✓ poor_single.csv exists")

    # Test 2: Read and parse the CSV file
    print("2. Testing CSV parsing...")
    try:
        with open(csv_path, 'r') as file:
            file_content = file.read()

        print("   ✓ File content read successfully")
        print(f"   Content length: {len(file_content)} characters")

        # Parse CSV like the Django view does
        csv_reader = csv.DictReader(io.StringIO(file_content))

        # Get the first row of data
        csv_data = {}
        for row in csv_reader:
            csv_data = {
                'pm25': row.get('PM2.5', ''),
                'pm10': row.get('PM10', ''),
                'no': row.get('NO', ''),
                'no2': row.get('NO2', ''),
                'nox': row.get('NOx', ''),
                'nh3': row.get('NH3', ''),
                'co': row.get('CO', ''),
                'so2': row.get('SO2', ''),
                'o3': row.get('O3', ''),
                'benzene': row.get('Benzene', ''),
                'toluene': row.get('Toluene', ''),
                'xylene': row.get('Xylene', '')
            }
            break  # Only process the first row

        print("   ✓ CSV parsed successfully")
        print("   Parsed data:")
        for key, value in csv_data.items():
            print(f"     {key}: '{value}'")

        # Check if all values are present
        empty_fields = [k for k, v in csv_data.items() if v == '']
        if empty_fields:
            print(f"   ⚠️  Warning: Empty fields found: {empty_fields}")
        else:
            print("   ✓ All fields have values")

    except Exception as e:
        print(f"   ❌ CSV parsing failed: {str(e)}")
        return False

    # Test 3: Check template rendering logic
    print("3. Testing template value rendering...")
    template_values = {}
    for key in ['pm25', 'pm10', 'no', 'no2', 'nox', 'nh3', 'co', 'so2', 'o3', 'benzene', 'toluene', 'xylene']:
        template_value = csv_data.get(key, '')
        template_values[key] = template_value
        print(f"   Template value for {key}: '{template_value}'")

    # Test 4: Simulate Django context
    print("4. Simulating Django template context...")
    context = {
        'uploaded_file_url': '/media/poor_single.csv',
        'csv_data': csv_data,
        'file_uploaded': True,
        'prediction_result': {'predicted_aqi': 234.13, 'category': 'Poor', 'color': 'red'}
    }

    print("   Context keys:", list(context.keys()))
    print("   csv_data keys:", list(context['csv_data'].keys()))
    print("   file_uploaded:", context['file_uploaded'])

    # Test 5: Check what the HTML would render
    print("5. Expected HTML form field values:")
    for field_name in ['pm25', 'pm10', 'no', 'no2', 'nox', 'nh3', 'co', 'so2', 'o3', 'benzene', 'toluene', 'xylene']:
        html_value = context['csv_data'].get(field_name, '')
        print(f"   <input value=\"{html_value}\"> for {field_name}")

    print("\n" + "=" * 50)
    print("DEBUG COMPLETE")
    print("If you're not seeing form fields filled after upload:")
    print("1. Check browser developer tools for JavaScript errors")
    print("2. Check Django server logs for errors")
    print("3. Verify the uploaded file is actually a CSV with correct headers")
    print("4. Check if the page is refreshing and losing the context")
    print("=" * 50)

    return True

if __name__ == "__main__":
    debug_csv_upload()
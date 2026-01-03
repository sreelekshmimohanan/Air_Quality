from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect,get_object_or_404
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings
from .models import *
from django.contrib import messages
import os
import pandas as pd
import joblib
import json
import csv
import io

def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')


def reg(request):
    return render(request,'register.html')


def addreg(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print('POST data:', request.POST)  # Debug print
        if not all([name, email, phone, password]):
            return render(request, 'register.html', {'message': "All fields are required!", 'error': True})
        try:
            ins = register(name=name, email=email, phone=phone, password=password)
            ins.save()
            return render(request, 'register.html', {'message': "Successfully Registered"})
        except Exception as e:
            return render(request, 'register.html', {'message': f"Error: {e}", 'error': True})
    return render(request, 'register.html')

def login(request):
     return render(request,'login.html')
    



def addlogin(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    if email=='admin@gmail.com' and password =='admin':
        request.session['logint']=email
        return render(request,'index.html')
    elif register.objects.filter(email=email,password=password).exists():
        user=register.objects.get(email=email,password=password)
        request.session['uid']=user.id
        return render(request,'index.html')
    else:
        return render(request,'login.html')
    



def logout(request):
    session_keys=list(request.session.keys())
    for key in session_keys:
          del request.session[key]
    return redirect(first)

def viewuser(request):
    data=register.objects.all()
    return render(request,'viewuser.html',{'data':data})

def upload(request):
    return render(request,'upload.html', {
        'pm25': '',
        'pm10': '',
        'no': '',
        'no2': '',
        'nox': '',
        'nh3': '',
        'co': '',
        'so2': '',
        'o3': '',
        'benzene': '',
        'toluene': '',
        'xylene': '',
    })

def addupload(request):
    if request.method == 'POST' and request.FILES['fileupload']:
        file = request.FILES['fileupload']

        # Extract CSV data and convert to JSON
        file.seek(0)  # Reset file pointer
        csv_data = csv.DictReader(io.StringIO(file.read().decode('utf-8')))
        data_list = list(csv_data)
        json_data = json.dumps(data_list)


        print("json_data:", json_data)  # Debug print
        csv_dict = data_list[0] if data_list else {}
        print("csv_dict:", csv_dict)  # Debug print

        return render(request, 'upload.html', {
            'json_data': json_data,
            'file_uploaded': True,
            'pm25': csv_dict.get('PM2.5', ''),
            'pm10': csv_dict.get('PM10', ''),
            'no': csv_dict.get('NO', ''),
            'no2': csv_dict.get('NO2', ''),
            'nox': csv_dict.get('NOx', ''),
            'nh3': csv_dict.get('NH3', ''),
            'co': csv_dict.get('CO', ''),
            'so2': csv_dict.get('SO2', ''),
            'o3': csv_dict.get('O3', ''),
            'benzene': csv_dict.get('Benzene', ''),
            'toluene': csv_dict.get('Toluene', ''),
            'xylene': csv_dict.get('Xylene', ''),
        })
    return render(request, 'upload.html')

def predict_aqi(request):
    """Handle AQI prediction from user input"""
    if request.method == 'POST':
        try:
            # Get pollutant values from form
            pollutants = {
                'PM2.5': float(request.POST.get('pm25', 0)),
                'PM10': float(request.POST.get('pm10', 0)),
                'NO': float(request.POST.get('no', 0)),
                'NO2': float(request.POST.get('no2', 0)),
                'NOx': float(request.POST.get('nox', 0)),
                'NH3': float(request.POST.get('nh3', 0)),
                'CO': float(request.POST.get('co', 0)),
                'SO2': float(request.POST.get('so2', 0)),
                'O3': float(request.POST.get('o3', 0)),
                'Benzene': float(request.POST.get('benzene', 0)),
                'Toluene': float(request.POST.get('toluene', 0)),
                'Xylene': float(request.POST.get('xylene', 0))
            }

            # Load ML model and scaler
            model_path = os.path.join(settings.BASE_DIR, 'ML', 'rf_reg_model.pkl')
            scaler_path = os.path.join(settings.BASE_DIR, 'ML', 'scaler_reg.pkl')

            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)

            # Prepare features for prediction
            required_features = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
            input_data = [[pollutants.get(feature, 0) for feature in required_features]]
            input_df = pd.DataFrame(input_data, columns=required_features)

            # Scale the input
            scaled_input = scaler.transform(input_df)

            # Make prediction
            predicted_aqi = model.predict(scaled_input)[0]

            # Save to database
            user_id = request.session.get('uid', 'anonymous')
            aqi_prediction = AQIPrediction(
                user_id=user_id,
                predicted_aqi=round(predicted_aqi, 2)
            )
            aqi_prediction.set_features_dict(pollutants)
            aqi_prediction.save()

            # Determine AQI category
            if predicted_aqi <= 50:
                category = "Good"
                color = "green"
            elif predicted_aqi <= 100:
                category = "Satisfactory"
                color = "yellow"
            elif predicted_aqi <= 200:
                category = "Moderate"
                color = "orange"
            elif predicted_aqi <= 300:
                category = "Poor"
                color = "red"
            elif predicted_aqi <= 400:
                category = "Very Poor"
                color = "purple"
            else:
                category = "Severe"
                color = "maroon"

            return render(request, 'upload.html', {
                'predicted_aqi': round(predicted_aqi, 2),
                'category': category,
                'color': color,
                'pollutants': pollutants,
                'success': True
            })

        except Exception as e:
            return render(request, 'upload.html', {
                'error': f"Prediction failed: {str(e)}"
            })

    return render(request, 'upload.html')

def view_predictions(request):
    """View user's AQI prediction history"""
    if request.session.get('logint'):  # admin
        predictions = AQIPrediction.objects.all().order_by('-prediction_date')
        # Add user name to each prediction
        for pred in predictions:
            try:
                user_id = int(pred.user_id)
                user = register.objects.get(id=user_id)
                pred.user_name = user.name
                pred.user_email = user.email
            except (ValueError, register.DoesNotExist):
                pred.user_name = 'Unknown'
                pred.user_email = 'N/A'
    else:
        user_id = request.session.get('uid')
        if user_id:
            predictions = AQIPrediction.objects.filter(user_id=user_id).order_by('-prediction_date')
        else:
            predictions = []

    return render(request, 'predictions.html', {'predictions': predictions, 'is_admin': bool(request.session.get('logint'))})
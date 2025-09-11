# predictor/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
import numpy as np
import os

# Load the model and scaler once when the server starts
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained_model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'scaler.pkl')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model and Scaler loaded successfully!")
except Exception as e:
    print(f" Error loading model: {e}")
    model = None
    scaler = None

def home(request):
    """Render the main page"""
    return render(request, 'predictor/index.html')
def ml_roadmap(request):
    return render(request, 'predictor/ml_roadmap.html')

@csrf_exempt  # For simplicity, disable CSRF protection for this view
def predict(request):
    """Handle prediction requests"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
    if model is None or scaler is None:
        return JsonResponse({'error': 'Model not loaded. Please check the server.'})
    
    try:
        # Get data from POST request
        overall_qual = float(request.POST.get('overall_qual'))
        gr_liv_area = float(request.POST.get('gr_liv_area'))
        garage_cars = float(request.POST.get('garage_cars'))
        total_bsmt_sf = float(request.POST.get('total_bsmt_sf'))
        year_built = float(request.POST.get('year_built'))
        
        features = [overall_qual, gr_liv_area, garage_cars, total_bsmt_sf, year_built]
        final_features = np.array(features).reshape(1, -1)
        final_features_scaled = scaler.transform(final_features)
        
        prediction = model.predict(final_features_scaled)
        output = round(prediction[0], 2)
        formatted_prediction = f"${output:,.2f}"
        
        return JsonResponse({'prediction': formatted_prediction})
    
    except Exception as e:
        return JsonResponse({'error': str(e)})
# views.py
import audioread
import os  # Import the os module
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from .forms import LungSoundUploadForm
from .utils import gru_diagnosis_prediction

def predict_respiratory_disease(request):
    if request.method == 'POST':
        form = LungSoundUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to a temporary location
            uploaded_file = request.FILES['lung_sound']
            temp=r"C:\Users\abujo\DjangoRDD\temp"
            file_path = os.path.join(temp, uploaded_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            try:
                # Load audio file using librosa
                classpreds, confidence = gru_diagnosis_prediction(file_path)
            except Exception as e:
                return JsonResponse({'error': 'Error loading audio file.'}, status=500)
            # Call the prediction function
            
            
            
            # Delete the temporary file
            os.remove(file_path)
            confidence = np.float64(confidence)
            # Return the prediction results
            return JsonResponse({'classpreds': classpreds, 'confidence': confidence})
    else:
        form = LungSoundUploadForm()
    return render(request, 'upload_form.html', {'form': form})

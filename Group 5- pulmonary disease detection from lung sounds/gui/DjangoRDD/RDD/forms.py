# forms.py
from django import forms

class LungSoundUploadForm(forms.Form):
    lung_sound = forms.FileField(label='Upload Lung Sound File', help_text='Accepts .wav files only')

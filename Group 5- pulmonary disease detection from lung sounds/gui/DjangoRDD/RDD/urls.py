from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Redirect root URL to the upload page
    path('', RedirectView.as_view(pattern_name='upload'), name='home'),

    # Define the URL pattern for the upload page
    path('upload/', views.predict_respiratory_disease, name='upload'),
    # Other URL patterns...
]
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
        path('training/', training, name="training_page"),
        path('pushup/', pushup, name="training_pushup"),
        path('dumbbell/', dumbbell, name="training_dumbbell"),
        path('barbell/', barbell, name="training_barbell"),
    ]
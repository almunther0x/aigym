from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('exercise/', views.exercise, name='exercisepage'),
    path('sports/<str:section>', views.sportsView, name='sportspage'),
    path('bmi/', views.bmiView, name='bmipage'),
    path('caloris/', views.calorisView, name='calorispage'),
    path('login/', views.loginView, name='loginpage'),
    path('profile/', views.profileView, name='profilepage'),
    path('exercise-history/', views.exerciseHistoryView, name='exercisehistorypage'),
    path('logout/', views.logout_view, name='logoutpage'),
    path('thanks/', views.thankyouView, name='thankspage'),
    path('exercises/<str:gender>/<str:page>/', views.muscleExercise, name='musclexercisepage'),
    path('me/', views.mastring_exercis, name='mastring_exercises'),
    path('foodcounter/', views.foodcounter, name='foodcounterpage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
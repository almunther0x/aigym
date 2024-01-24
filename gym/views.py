from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.db.models import Max, Count
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import logout, login
import requests, json, random
import numpy as np
from datetime import datetime, date
from .models import Sports, Exercises, Meals, Profile
from .forms import ProfileForm

# Create home views.
def home(request):
    sports_list = Sports.objects.filter(section='sport').values()
    injuries_list = Sports.objects.filter(section='injuries').values()
    user = request.user.is_authenticated

    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        subject = "Fitness Center Website: New message from " + first_name + ' ' + last_name
        email = request.POST["email"]
        message = request.POST["message"]
        if subject and message and email:
            try:
                msg = EmailMessage(subject, message, "almonther55546@gmail.com", ["almonther55546@gmail.com"])
                msg.send()
            except Exception as err:
                print(err)
                return render(request, 'index.html', { 'user': user, 'error_msg': True, 'sports_list': sports_list, 'injuries_list': injuries_list})
            return HttpResponseRedirect("thanks/")
    else:
        return render(request, 'index.html', { 'user': user, 'sports_list': sports_list, 'injuries_list': injuries_list})
    
# sports page
def sportsView(request, section):
    details = Sports.objects.filter(title=section.capitalize()).values()
    context = {
        'section': section,
        'details': details
    }

    return render(request, 'sports.html', context)

# sports page
def exerciseHistoryView(request):
    if request.user.is_authenticated:
        month = datetime.now().month
        if request.method == 'POST':
            month = request.POST['month']

        year = datetime.now().year
        user = request.user.id
        exercises = Exercises.objects.filter(user_id = user, exercise_date__year = year, exercise_date__month = month).order_by('-id').values()
        
        max_count = exercises.aggregate(Max('exercise_value'))

        monthsList = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]

        return render(request, 'history.html', {'exercises': exercises, 'max_count': max_count, 'monthsList': monthsList, 'month': month, 'year': year})
    else:
        return redirect("/login")

def profileView(request):
    try:
        _profile = Profile.objects.get(user=request.user.id)
    except:
        _profile = None
    user = User.objects.get(id=request.user.id)
    form = ProfileForm(initial={'user': request.user.id})

    if _profile:
        image = _profile.image.url
    else:
        image = 'default.jpg'

    profileData = {
        'image': image,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    if request.method == 'POST':
        user.first_name =  request.POST['first_name']
        user.last_name =  request.POST['last_name']
        user.email =  request.POST['email']
        if request.POST['password']:
            user.set_password(request.POST['password'])
        user.save()
        if _profile:
            form = ProfileForm(request.POST, request.FILES, instance=_profile)
        else:
            form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        
        return redirect("/logout")
    else:
        return render(request, 'profile.html', {'profileData': profileData, 'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

# display exercise page or redirect if not login.
def exercise(request):
    if request.user.is_authenticated:
        return render(request, 'exercise.html')
    else:
        return redirect("/login")

def muscleExercise(request, gender, page):
    if request.user.is_authenticated:
        page_path = '/static/exercises/'+gender+'/'+page+'.html'

        return render(request, 'muscle_exercise.html', {'page': page_path})
    else:
        return redirect("/login")

def foodcounter(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            query = request.POST['query']
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
            api_request = requests.get(
                api_url + query, headers={'X-Api-Key': 'Rh9ET7fsTxphIuLPOoJcqw==h8Td2ucwhj4aOBmU'})
            try:
                api = json.loads(api_request.content)
            except Exception as e:
                api = "oops! There was an error"
            return render(request, 'foodcounter.html', {'api': api})
        else:
            return render(request, 'foodcounter.html', {'query': 'Enter a valid query'})
    else:
        return redirect("/login")
    
def mastring_exercis(request):
    return render(request, 'me.html')
    

def thankyouView(request):
    return render(request, 'thankyou.html')

# login view
def loginView(request):
    if request.user.is_authenticated:
       return redirect("/")

    if request.method == 'POST':
        action_type =  request.POST["action_type"]
        if action_type == 'login':
            username = request.POST["login_username"]
            password = request.POST["login_password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request=request, user=user)

                return redirect("home")
            else:
                return render(request, 'login.html', {'login_error': True})
        else:
            username_unique_error = False
            email_unique_error = False
            # check if user does not exist
            if User.objects.filter(username=request.POST["username"]).exists():
                username_unique_error = True

            if User.objects.filter(email=request.POST["email"]).exists():
                email_unique_error = True
            

            if not email_unique_error and not username_unique_error:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.is_active = True

                user.save()
                return redirect("/")
            else:
                return render(request, 'login.html', {'signup_error': True})
    else:
        return render(request, 'login.html')

# calculate calories by user inbut
def calorisView(request):
    if request.method == 'POST':
        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
        query = request.POST["input"]
        response = requests.get(api_url + query, headers={'X-Api-Key': 'HRBuACb6HPW9LOHTfI0UaA==JD8dQGT5Ec9Td3hr'})
        if response.status_code == requests.codes.ok:
            return render(request, 'caloris.html', { 'response': response.json})
        else:
            return render(request, 'caloris.html', { 'error': True})
    else:
        return render(request, 'caloris.html')

# calculate bmi by user inbut
def bmiView(request):
    if request.method == 'POST':
        age = request.POST["age"]
        height = request.POST['height']
        weight = request.POST["weight"]
        gender = request.POST["gender"]
        activity = request.POST["activity"]
        goalweight = request.POST["goalweight"]

        results = calculate_bmi(height, weight, age, activity, gender, goalweight)
        meals_list = None

        if results:
            limit = 500
            limit_lt = 1500
            try:
                if(int(results.bmr) > 2000):
                    limit = 1000
                    limit_lt = 2500
            except:
                pass
            meals_list = Meals.objects.filter(meal_kcal__gte = limit, meal_kcal__lte = limit_lt).order_by('?').values()
            num = 0
            meal_choices = []

            for index in range(7):
                daily_meals = []
                for inx in range(3):
                    daily_meals.append(meals_list[num])
                    num = num + 1
                meal_choices.append(daily_meals)  # Append the first 3 meals of the day to the list
        
        return render(request, 'bmi.html', { 'results': results, 'meals_list': meal_choices})
    else:
        if request.user.is_authenticated:
            return render(request, 'bmi.html')
        else:
            return redirect("/login")
        

def calculate_bmi(height, weight, age, activity_level, gender, goal_weight):
    weight = int(weight)
    height = int(height)
    age = int(age)
    goal_weight = int(goal_weight)
    daily_calories = 0
    # BMI calculation​
    height_in_meters = height / 100  # Convert height to meters
    bmi = weight / (height_in_meters ** 2)

    if bmi < 18.4:
        weight_status = "Underweight"
    elif bmi >= 18.5 and bmi <= 25:
        weight_status = "Normal weight"
    elif bmi >= 25 and bmi < 30:
        weight_status = "Overweight"
    else:
        weight_status = "Obese"
        
    if gender == 'male':
        g_val = 5
    else:
        g_val = 161

    bmr = (10 * weight) + (6.25 * height) - (5 * age) + g_val
    
    activity_multiplier = {"none": 1.2, "light": 1.375, "moderate": 1.55, "heavy": 1.725, "xheavy": 1.9}
    raw_bmr = bmr * activity_multiplier.get(activity_level.lower()) 
    
    if(goal_weight > weight):
        daily_calories = raw_bmr + 500
        weight_for = 'to gain weight'
    else:
        daily_calories = raw_bmr - 500
        weight_for = 'to lose weight'

    print(bmr, daily_calories)

    return {
        "bmi": int(bmi),
        "weight_status": weight_status,
        "weight_for": weight_for,
        "goal_weight": goal_weight,
        "activity_level": activity_level,
        "raw_bmr": raw_bmr,
        "bmr": daily_calories,
    }

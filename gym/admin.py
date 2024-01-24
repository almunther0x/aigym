from django.contrib import admin
from .models import Sports, Exercises, Meals, Profile

# Register your models here.
admin.site.register(Sports)
admin.site.register(Exercises)
admin.site.register(Meals)
admin.site.register(Profile)
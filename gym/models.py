from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Sports(models.Model):
    image = models.TextField()
    title = models.TextField()
    about = models.TextField()
    link = models.TextField()
    section = models.TextField()
    background = models.TextField()

class Exercises(models.Model):
    exercise_date = models.DateField()
    exercise_type = models.TextField()
    exercise_value = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Meals(models.Model):
    meal_name = models.TextField()
    meal_kcal = models.IntegerField()
    meal_measure = models.TextField()
    meal_weight = models.CharField(max_length=255)
    meal_fat =  models.CharField(max_length=255)
    meal_carbo =  models.CharField(max_length=255)
    meal_protein =  models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile') # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance).save()
    except Exception as err:
        print('Error creating user profile!')
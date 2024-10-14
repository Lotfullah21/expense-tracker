from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomManager

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15,unique =True)
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=[("Male", "Male"), ("Female", "Female")])
    profile_picture = models.ImageField(upload_to="files/image/profile")
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["age", "gender"]
    objects = CustomManager()


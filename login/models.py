from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    user_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)

    def __str__(self):
        return self.user_name



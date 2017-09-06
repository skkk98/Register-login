from django.db import models
from django.contrib.auth.models import User

class Userss(models.Model):
    Username = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.IntegerField()



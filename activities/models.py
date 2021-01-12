from django.db import models
from accounts.models import User

# Create your models here.


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repo = models.CharField(max_length=255)
    grade = models.IntegerField(null=True)

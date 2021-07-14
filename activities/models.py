from django.db import models
from accounts.models import User


class Activity(models.Model):
    title = models.CharField(max_length=255)
    points = models.IntegerField(null=True)


class Submission(models.Model):
    grade = models.IntegerField(null=True, blank=True)
    repo = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='submissions', null=True)
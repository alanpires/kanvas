from django.db import models
from django.contrib.auth.models import AbstractUser
from courses.models import Course

class User(AbstractUser):
    courses = models.ManyToManyField(Course, related_name="users")

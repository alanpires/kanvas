from rest_framework import serializers
from accounts.models import UserSerializer


class Courses(serializers.Serializer):
    name = models.CharField
    users = UserSerializer(many=True)

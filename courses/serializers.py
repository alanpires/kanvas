from accounts.serializers import UserSerializer, UsernameSerializer
from rest_framework import serializers
from activities.serializers import ActivitySerializer

class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    users = UsernameSerializer(many=True, read_only=True)
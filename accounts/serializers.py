from rest_framework import serializers
from activities.serializers import ActivitySerializer


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    activity_set = ActivitySerializer(many=True, read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

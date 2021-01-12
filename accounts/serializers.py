from rest_framework import serializers
from activities.serializers import ActivitySerializer


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    activity_set = ActivitySerializer(many=True, read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

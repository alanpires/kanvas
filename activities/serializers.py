from rest_framework import serializers


class ActivitySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    repo = serializers.CharField()
    grade = serializers.CharField()

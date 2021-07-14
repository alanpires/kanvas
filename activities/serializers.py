from accounts.models import User
from rest_framework import serializers
from accounts.serializers import UsernameSerializer
 
class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    grade = serializers.IntegerField(required=False)
    repo = serializers.CharField()
    user_id = serializers.IntegerField(read_only=True)
    activity_id = serializers.IntegerField(read_only=True)


class SubmissionGradingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    grade = serializers.IntegerField()
    repo = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    activity_id = serializers.IntegerField(read_only=True)


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    points = serializers.IntegerField()
    submissions = SubmissionSerializer(many=True, read_only=True)
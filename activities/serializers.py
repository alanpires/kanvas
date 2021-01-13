from rest_framework import serializers


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    repo = serializers.CharField()
    grade = serializers.IntegerField(required=False)

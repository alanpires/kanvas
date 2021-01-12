from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer
from .permissions import FacilitatorEditProtected
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

# Create your views here.


class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [FacilitatorEditProtected]

    def put(self, request):
        serializer = ActivitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        activity = Activity(**request.data)
        activity.save()

        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = ActivitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        activity = Activity.objects.create(**serializer.data)
        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        if not user_id and not activity_id:

            queryset = Activity.objects.all()
            serializer = ActivitySerializer(queryset)

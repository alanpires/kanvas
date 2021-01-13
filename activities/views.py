from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer
from .permissions import FacilitatorEditProtected
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import ipdb

# Create your views here.


class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [FacilitatorEditProtected, IsAuthenticated]

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

    def get(self, request, user_id=''):
        user = request.user

        if not user.is_staff:
            queryset = Activity.objects.filter(user=user)
            serializer = ActivitySerializer(queryset, many=True)
            return Response(serializer.data)

        else:
            if user_id:
                queryset = Activity.objects.filter(user_id=user_id)
                serializer = ActivitySerializer(queryset, many=True)
                return Response(serializer.data)

            queryset = Activity.objects.all()
            serializer = ActivitySerializer(queryset, many=True)
            return Response(serializer.data)

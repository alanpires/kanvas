from django.shortcuts import render
from rest_framework.views import APIView
from .models import Activity

# Create your views here.


class ActivityView(APIView):
    def get(self, request, user_id='', activity_id):
        if not user_id and not activity_id:

            queryset = Activity.objects.all()
            serializer =

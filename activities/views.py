from django.shortcuts import render
from rest_framework import response, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Activity, Submission
from .serializers import ActivitySerializer, SubmissionSerializer, SubmissionGradingSerializer
from .permissions import IsInstructorOrFacilitator, IsStudent
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from courses.models import Course
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import User


class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructorOrFacilitator]

    def post(self, request):   
        serializer = ActivitySerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
        activity = Activity.objects.get_or_create(title=request.data['title'])[0]
        activity.points = request.data['points']
        activity.save()
        
        serializer = ActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ActivitySubmissionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStudent]
    
    def post(self, request, activity_id):
        serializer = SubmissionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('grade'):
            grade = request.data.pop('grade')
        
        activity = Activity.objects.get(id=activity_id)
        submission = Submission.objects.create(**request.data, user=request.user, activity=activity)
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubmissionGradingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructorOrFacilitator]
    
    def put(self, request, submission_id):
        serializer = SubmissionGradingSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        submission = Submission.objects.get(id=submission_id)
        submission.grade = request.data['grade']
        submission.save()
        
        serializer = SubmissionGradingSerializer(submission)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SubmissionListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        submissions = Submission.objects.all()
        
        if request.user.is_staff == False and request.user.is_superuser == False:
            submissions = Submission.objects.filter(user=request.user)
        
        serializer = SubmissionSerializer(submissions, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

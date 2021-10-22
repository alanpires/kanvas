from django.shortcuts import get_object_or_404
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
from django.db.utils import IntegrityError

class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructorOrFacilitator]

    def post(self, request):   
        serializer = ActivitySerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        try:
            activity = Activity.objects.create(
                title=serializer.validated_data.get('title'),
                points=serializer.validated_data.get('points', None)
            )
        except IntegrityError:
            return Response({ 'error': 'Activity with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ActivityDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructorOrFacilitator]
    
    def put(self, request, *args, **kwargs):
        serializer = ActivitySerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        activity = get_object_or_404(Activity, id=kwargs.get('activity_id', None))
        
        if activity.submissions.count() > 0:
            return Response({ 'error': 'You can not change an Activity with submissions'}, status=status.HTTP_400_BAD_REQUEST)
        
        activity.title = request.data.get('title')
        activity.points = request.data.get('points', None)
        
        try:
            activity.save()
        except IntegrityError:
            return Response({ 'error': 'Activity with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = ActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
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

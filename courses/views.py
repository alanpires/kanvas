from django.db.utils import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Course
from accounts.models import User
from .serializers import CourseSerializer
from .permissions import IsInstructorOrReadOnly
from rest_framework.authentication import TokenAuthentication


class CourseRegistrationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructorOrReadOnly]

    def put(self, request, course_id):
        user_ids = request.data.get('user_ids')

        if not isinstance(user_ids, list):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)

        except ObjectDoesNotExist:
            return Response({'errors': 'invalid course_id'}, status=status.HTTP_404_NOT_FOUND)

        users = []
        user_ids = request.data['user_ids']

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                users.append(user)

            except ObjectDoesNotExist:
                return Response({'errors': 'invalid user_id list'}, status=status.HTTP_400_BAD_REQUEST)

        users_denied = []

        for user in users:
            if user.is_staff:
                users_denied.append(user)

        if users_denied:
            return Response({'errors': 'Only students can be enrolled in the course.'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            for user in users:
                course.users.add(user)

        associated_users = course.users.all()
        for user in associated_users:
            if user.id not in user_ids:
                course.users.remove(user)

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructorOrReadOnly]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.create(**serializer.validated_data)
        except IntegrityError:
            return Response({ 'error': 'Course with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, course_id=''):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)

        if course_id:
            try:
                queryset = Course.objects.get(id=course_id)
                serializer = CourseSerializer(queryset)
            except ObjectDoesNotExist:
                return Response({'errors': 'invalid course_id'}, status=status.HTTP_404_NOT_FOUND) 

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CourseSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        course.name = serializer.validated_data.get('name')
        
        try:
            course.save()
        except IntegrityError:
            return Response({ 'error': 'Course with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
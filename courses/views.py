from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Course
from accounts.models import User
from .serializers import CourseSerializer
import ipdb


class CourseRegistrationView(APIView):

    def put(self, request):
        course_id = request.data.get('course_id')
        user_ids = request.data.get('user_ids')

        if not isinstance(course_id, int):
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
                return Response({'errors': 'invalid user_id list'}, status=status.HTTP_404_NOT_FOUND)

        for user in users:
            course.user_set.add(user)

        associated_users = course.user_set.all()
        for user in associated_users:
            if user.id not in user_ids:
                course.user_set.remove(user)

        serializer = CourseSerializer(course)
        return Response(serializer.data)


class CourseView(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.create(**request.data)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, user_id=''):
        queryset = Courses.objects.all()

        if user_id:
            queryset = Courses.objects.filter(user_id=user_id)

        serializer = CourseSerializer(queryset, many=True)

        return Response(serializer.data)

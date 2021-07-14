from django.urls import path
from .views import CourseView, CourseRegistrationView

urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/<int:course_id>/', CourseView.as_view()),
    path('courses/<int:course_id>/registrations/', CourseRegistrationView.as_view())
]

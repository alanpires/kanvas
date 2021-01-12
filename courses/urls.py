from django.urls import path
from .views import CourseView, CourseRegistrationView

urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/registrations/', CourseRegistrationView.as_view())
]

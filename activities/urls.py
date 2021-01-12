from django.urls import path
from .views import ActivityView

urlpatterns = [
    path('activities/', ActivityView.as_view())
]

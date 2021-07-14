from django.urls import path
from .views import ActivityView, ActivitySubmissionView, SubmissionGradingView, SubmissionListView

urlpatterns = [
    path('activities/', ActivityView.as_view()),
    path('activities/<int:activity_id>/submissions/', ActivitySubmissionView.as_view()),
    path('submissions/<int:submission_id>/', SubmissionGradingView.as_view()),
    path('submissions/', SubmissionListView.as_view())
]
from django.urls import path
from .views import LoginView, AccountsView

urlpatterns = [
    path('accounts/', AccountsView.as_view()),
    path('login/', LoginView.as_view())
]

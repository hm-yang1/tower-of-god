from django.contrib import admin
from django.urls import path
from .views.user_views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
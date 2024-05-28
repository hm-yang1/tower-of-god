import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework import permissions, status
from ..serial.user_serializer import UserRegisterSerializer, UserSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # Not sure if validation here or frontend
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
                
    def post(self, request):
        # Disallow user from logging in again
        if request.user.is_authenticated:
            return Response({'Already logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        
        username = request.data['username']
        password = request.data['password']
        
        # Use authenticate or use Object.get + check_password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({'Incorrect login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({'Logout success'}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    pass

class HistoryView(APIView):
    pass

class FavoritesView(APIView):
    pass
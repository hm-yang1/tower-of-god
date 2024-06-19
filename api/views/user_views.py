import os
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
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
        return Response({'error': 'Invalid data'}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
                
    def post(self, request):
        # Disallow user from logging in again, works only if sends bearer token
        print(request.user)
        if request.user.is_authenticated:
            return Response({'error': 'Already logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        
        username = request.data['username']
        password = request.data['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Incorrect login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Getting refresh token
        refresh_token = request.headers.get('refresh-token')
        print(refresh_token)

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({'success': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Invalid or expired token.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(APIView):
    pass
    
class FavoritesView(APIView):
    pass
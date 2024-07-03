import os
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied, NotAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.backends.google import GoogleOAuth2
from social_django.utils import load_backend, load_strategy
from ..serial.user_serializer import UserRegisterSerializer, UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Not sure if validation here or frontend
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
                
    def post(self, request):
        # Disallow user from logging in again, works only if sends bearer token
        if request.user.is_authenticated:
            return Response({'error': 'Already logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.data.get('username'):
            return Response({'error':'No username or password'}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('password'):
            return Response({'error':'No username or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        username = request.data['username']
        password = request.data['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            # Update last_login time
            user.last_login = timezone.now()
            user.save()
            
            # Generate new refresh token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Incorrect login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Getting refresh token
        refresh_token = request.headers.get('refresh-token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({'success': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Invalid or expired token.", "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        google_url = settings.GOOGLE_LOGIN_URL
        
        if google_url:
            return Response({'url': google_url}, status=status.HTTP_200_OK)
        else:
            raise NotFound('Google login url not found')
        
    def post(self, request, *args, **kwargs):
        strategy = load_strategy(request)
        # backend = load_backend(strategy, 'google-oauth2', redirect_uri=None)
        backend = GoogleOAuth2()
        
        google_code = request.data.get('code', None)
        if not google_code:
            raise ParseError('Google code not found')
        
        # Try login/create user
        try:
            access_token = self.get_google_access_token(google_code)
            
            # Check google token with social auth
            user = backend.do_auth(access_token)
            if not user:
                raise PermissionDenied('Failed Google login. Invalid token.')
            
            # Update last_login time
            user.last_login = timezone.now()
            
            # Minor incoveneience of google login where email and username are different
            user.username = user.email
            user.save()
            
            # Generate simple jwt token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_google_access_token(self, code):
        token_url = 'https://oauth2.googleapis.com/token'
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        redirect_uri = settings.CALLBACK_URL_ON_GOOGLE
        
        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=data)
        response_data = response.json()

        if response.status_code == 200:
            return response_data.get('access_token')
        else:
            raise NotFound('Failed to convert google authorise code to google access token' + str(response))
            
class ProfileView(APIView):
    pass
    
class FavoritesView(APIView):
    pass
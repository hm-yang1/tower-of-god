from atexit import register
from urllib import response
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from ..models.user import User
from ..serial.user_serializer import UserRegisterSerializer, UserSerializer

class UserViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Add user for testing
        self.user = User.objects.create_user(
            username = 'testing@gmail.com',
            password = '123'
        )
    
    ########## Register tests ##########
    def test_register(self):
        response = self.client.post(
            reverse('register'),
            {
                "username": "test1@gmail.com",
                "password": "123"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_exists = User.objects.filter(username='test1@gmail.com').exists()
        self.assertTrue(user_exists)
        
    def test_register_existing_username(self):
        response = self.client.post(
            reverse('register'),
            {
                "username": "testing@gmail.com",
                "password": "123"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_register_no_username(self):
        response = self.client.post(
            reverse('register'),
            {
                "password": "123"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_register_invalid_username(self):
        response = self.client.post(
            reverse('register'),
            {
                "username": "bobby bo",
                "password": "123"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_register_no_password(self):
        response = self.client.post(
            reverse('register'),
            {
                "username": "temp@gmail.com",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_password(self):
        response = self.client.post(
            reverse('register'),
            {
                "username": "temp@gmail.com",
                "password": ""
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    ########## Login tests ##########
    def test_login(self):
        user_exists = User.objects.filter(username='testing@gmail.com').exists()
        self.assertTrue(user_exists)
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testing@gmail.com',
                'password': '123'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        return response
        
    def test_login_no_username(self):
        response = self.client.post(
            reverse('login'),
            {
                "password": "123"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_invalid_username(self):
        response = self.client.post(
            reverse('login'),
            {
                "username": "bobby bo",
                "password": "123"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_login_no_password(self):
        response = self.client.post(
            reverse('login'),
            {
                "username": "testing@gmail.com",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_password(self):
        response = self.client.post(
            reverse('login'),
            {
                "username": "testing@gmail.com",
                "password": "wrong password"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    ########## Logout tests ##########
    def test_logout(self):
        # Login first
        response = self.test_login()
        refresh = response.data.get('refresh')
        access = response.data.get('access')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        headers = {
            'refresh-token':refresh
        }
        
        response = self.client.post(
            reverse('logout'),
            {},
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout_invalid_access(self):
        response = self.test_login()
        refresh = response.data.get('refresh')
        access = response.data.get('access')
        access = str(access) + 'really bad access'
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        headers = {
            'refresh-token': refresh
        }
        response = self.client.post(
            reverse('logout'),
            {},
            **headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_logout_missing_access(self):
        response = self.test_login()
        refresh = response.data.get('refresh')
        access = response.data.get('access')
        self.client.credentials()
        headers = {
            'refresh-token': refresh
        }
        response = self.client.post(
            reverse('logout'),
            {},
            headers=headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_logout_invalid_refresh(self):
        response = self.test_login()
        refresh = response.data.get('refresh')
        access = response.data.get('access')
        refresh = str(refresh) + 'really bad'
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        headers = {
            'refresh-token': refresh
        }
        response = self.client.post(
            reverse('logout'),
            {},
            headers=headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout_missing_refresh(self):
        response = self.test_login()
        refresh = response.data.get('refresh')
        access = response.data.get('access')
        self.client.credentials()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.post(
            reverse('logout'),
            {},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
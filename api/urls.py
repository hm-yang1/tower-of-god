from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.user_views import LoginView, LogoutView, RegisterView
from .views.category_view import CategoryView
from .views.product_views import ProductViewSet

# router to add product view sets
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Authentication Urls
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    
    # Get URLs
    path('categories/', CategoryView.as_view()),
    path('', include(router.urls))
]
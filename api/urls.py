from posixpath import basename
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.wishlist_views import WishlistViewSet
from .views.user_views import LoginView, LogoutView, RegisterView
from .views.product_views import ProductViewSet
from .views.comparison_views import ComparisonViewSet

# router to add product view sets
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'compare', ComparisonViewSet, basename='compare')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    # Authentication Urls
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Get URLs
    path('', include(router.urls)),
]
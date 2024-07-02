from posixpath import basename
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.wishlist_views import WishlistViewSet
from .views.user_views import LoginView, LogoutView, RegisterView, RefreshTokenView
from .views.product_views import ProductViewSet
from .views.comparison_views import ComparisonViewSet
from rest_framework_simplejwt.views import TokenRefreshView

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
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Get URLs
    path('', include(router.urls)),
]

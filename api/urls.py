from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.user_views import LoginView, LogoutView, RegisterView
from .views.category_view import CategoryView
from .views.product_views import (
    EarbudsViewSet, 
    HeadphonesViewSet,
    KeyboardViewSet,
    LaptopViewSet,
    MouseViewSet,
)

# router to add product view sets
router = DefaultRouter()
router.register(r'earbuds', EarbudsViewSet)
router.register(r'headphones', HeadphonesViewSet)
router.register(r'keyboard', KeyboardViewSet)
router.register(r'laptop', LaptopViewSet)
router.register(r'mouse', MouseViewSet)

urlpatterns = [
    # Authentication Urls
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    
    # Get URLs
    path('categories/', CategoryView.as_view()),
    path('products/', include(router.urls))
]
import os
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models.monitor import Monitor
from ..models.speaker import Speaker
from ..models.television import Television
from ..models.earbuds import Earbuds
from ..models.keyboard import Keyboard
from ..models.laptop import Laptop
from ..models.mouse import Mouse
from ..models.phone import Phone
from .wishlist_views import WishlistViewSet
from ..models.search_history import SearchHistory, SearchHistorySerializer

# Edited version of search history, cannot fully inherit cause need to override too many things, no point
class SearchHistoryViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SearchHistorySerializer
        
    def get_queryset(self):
        user = self.request.user
        queryset = SearchHistory.objects.filter(user = user).order_by('-datetime')        
        return queryset
    
    def create(self, request, *args, **kwargs):        
        product_category = request.data.get('product_category')
        object_id = request.data.get('object_id')
        
        if not product_category or not object_id:
            return Response({"error": "Product category and object ID are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Determine the model class
        match product_category:
            case 'earbuds':
                product = Earbuds
            case 'keyboard':
                product = Keyboard
            case 'laptop':
                product = Laptop
            case 'mouse':
                product = Mouse
            case 'phone':
                product = Phone
            case 'television':
                product = Television
            case 'monitor':
                product = Monitor
            case 'speaker':
                product = Speaker
            case _:
                return Response({"error": "Invalid product category"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the object_id exists in the specified model
        try:
            product_instance = product.objects.get(id=object_id)
        except product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a search history item
        history_item = SearchHistory.objects.create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(product_instance),
            object_id=product_instance.id,
        )
        
        print(str(history_item))
        
        return Response({"message": "Search History item created successfully"}, status=status.HTTP_201_CREATED)
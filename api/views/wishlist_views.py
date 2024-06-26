import os
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models.monitor import Monitor
from ..models.speaker import Speaker
from ..models.television import Television
from ..models.earbuds import Earbuds
from ..models.keyboard import Keyboard
from ..models.laptop import Laptop
from ..models.mouse import Mouse
from ..models.phone import Phone
from ..serial.user_serializer import UserSerializer
from ..models.wishlist import Wishlist, WishlistSerializer

# Wishlist views

# View to get wishlist of user that sent the request
class WishlistViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = WishlistSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Wishlist.objects.filter(user = user).order_by('-datetime')        
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
        
        # Get content type
        content_type = ContentType.objects.get_for_model(product_instance)
        
        # Check if item already exist in wishlist
        queryset = self.get_queryset()
        if queryset.filter(content_type=content_type, object_id=object_id).exists():
            return Response({'error': 'Item already exists in your wishlist'}, status=status.HTTP_409_CONFLICT)

        # Create a wishlist item
        wishlist_item = Wishlist.objects.create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(product_instance),
            object_id=product_instance.id,
        )
        
        print(str(wishlist_item))
        
        return Response({"message": "Wishlist item created successfully"}, status=status.HTTP_201_CREATED)
    
    # No need for custom delete given model viewset provides default implementation
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
        
    #     queryset = self.get_queryset()
    #     wish = queryset.filter(id=instance.id)
    #     print(wish)
    #     if not wish.exists():
    #         return Response({"error": "Wish does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    #     wish.delete()
    #     return Response({"message": "Wishlist item deleted successfully"}, status=status.HTTP_200_OK)
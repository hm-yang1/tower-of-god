from unittest.util import _MAX_LENGTH
from django.db import models
from .user import User
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ..serial.user_serializer import UserSerializer
from .earbuds import Earbuds, EarbudSerializer
from .keyboard import Keyboard, KeyboardSerializer
from .laptop import Laptop, LaptopSerializer
from .mouse import Mouse, MouseSerializer
from .phone import Phone, PhoneSerializer
from .monitor import Monitor, MonitorSerializer
from .speaker import Speaker, SpeakerSerializer
from .television import Television, TelevisionSerializer

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_histories')
    
    # Using content types to identify product
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        result = self.user.username 
        result +=  '\n' + str(self.content_type)
        result += '\n' + str(self.content_object)
        result += '\n' + str(self.datetime)
        return result
    
class WishlistSerializer(serializers.ModelSerializer):
    # Serializes user
    user = UserSerializer()
    
    # Serializes product
    content_object = serializers.SerializerMethodField()
    
    class Meta:
        model = Wishlist
        fields = '__all__'
        
    def get_content_object(self, obj):
        content_type = obj.content_type
        model_class = content_type.model_class()
                
        if model_class == Earbuds:
            serializer_class = EarbudSerializer
        elif model_class == Keyboard:
            serializer_class = KeyboardSerializer
        elif model_class == Laptop:
            serializer_class = LaptopSerializer
        elif model_class == Mouse:
            serializer_class = MouseSerializer
        elif model_class == Phone:
            serializer_class = PhoneSerializer
        elif model_class == Speaker:
            serializer_class = SpeakerSerializer
        elif model_class == Monitor:
            serializer_class = MonitorSerializer
        elif model_class == Television:
            serializer_class = TelevisionSerializer
        else:
            serializer_class = serializers.Serializer

        serializer = serializer_class(instance=obj.content_object, context=self.context)
        return serializer.data
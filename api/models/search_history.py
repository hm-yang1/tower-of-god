from .wishlist import AbstractWishlist, AbstractWishlistSerializer
from django.db import models
from .user import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# SearchHistory is a copy of Wishlist
class SearchHistory(AbstractWishlist):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    
    class Meta:
        db_table = 'api_search_history'

class SearchHistorySerializer(AbstractWishlistSerializer):
    class Meta(AbstractWishlistSerializer.Meta):
        model = SearchHistory

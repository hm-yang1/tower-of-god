from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from ..models.user import User
from ..models.wishlist import Wishlist, WishlistSerializer

class WishlistViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = 'testing@gmail.com',
            password = '123'
        )
        self.wishlist = Wishlist.objects.create(
            
        )
    
    def test_add_wishlist(self):
        pass
    
    def test_get_wishlist(self):
        pass
    
    def test_delete_wishlist(self):
        pass
    
    # Incorrect Tests
    def test_unauthorised_add(self):
        pass
    
    def test_invalid_category_add(self):
        pass
    
    def test_invalid_product_id_add(self):
        pass
    
    def test_repeated_item_add(self):
        pass
    
    def test_unauthorised_get(self):
        pass
    
    def test_unauthorised_delete(self):
        pass
    
    def test_invalid_delete(self):
        pass
    
    
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from requests import delete
from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework import status
from ..models.earbuds import Earbuds
from ..models.keyboard import Keyboard
from ..models.laptop import Laptop
from ..models.monitor import Monitor
from ..models.mouse import Mouse
from ..models.phone import Phone
from ..models.speaker import Speaker
from ..models.television import Television
from ..models.user import User
from ..models.wishlist import Wishlist, WishlistSerializer

class WishlistViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = 'testing@gmail.com',
            password = '123'
        )
        
        self.alt_user = User.objects.create_user(
            username = 'test@gmail.com',
            password = '123'
        )
        
        self.earbuds = Earbuds.objects.create(
            name='test Earbuds',
            price=100.00,
            review_date='2023-06-21',
            wireless=True,
            battery_life=10.5,
            active_noise_cancellation=True
        )
        self.keyboard = Keyboard.objects.create(
            name='test Keyboard',
            price=150.00,
            review_date='2023-06-22',
            wireless=True,
            size=104,
            key_switches='Mechanical'
        )
        self.laptop = Laptop.objects.create(
            name='ASUS TUF Gaming A16',
            battery_life=['12.9 hrs (rtings.com)'],
            weight=2.2,
            screen_size=16.0,
            screen_resolution='1920 x 1200',
            processor='AMD Ryzen 7 7735HS',
            os_version='Windows 11',
        )
        self.monitor = Monitor.objects.create(
            name='test Monitor',
            price=300.00,
            review_date='2023-06-23',
            screen_size=27,
            screen_resolution='2560x1440',
            refresh_rate=144,
            panel_type='IPS'
        )
        self.mouse = Mouse.objects.create(
            name='test Mouse',
            price=50.00,
            review_date='2023-06-24',
            wireless=True,
            buttons_count=6,
            dpi=16000,
            weight=85.0
        )
        self.phone = Phone.objects.create(
            name='test Phone',
            price=800.00,
            review_date='2023-06-25',
            battery_life=[10, 12, 14],
            os_version='Android 12',
            size=6,
            screen_resolution='1080x2400',
            processor='Snapdragon 888'
        )
        self.speaker = Speaker.objects.create(
            name='test Speaker',
            price=150.00,
            review_date='2023-06-26',
            portable=True,
            bluetooth=True,
            wifi=True,
            speakerphone=True
        )
        self.television = Television.objects.create(
            name='test Television',
            price=1200.00,
            review_date='2023-06-27',
            screen_size=55,
            screen_resolution='3840x2160',
            panel_type='OLED'
        )
        
        # ContentType for the products
        self.earbuds_content_type = ContentType.objects.get_for_model(Earbuds)
        self.keyboard_content_type = ContentType.objects.get_for_model(Keyboard)
        self.monitor_content_type = ContentType.objects.get_for_model(Monitor)
        self.mouse_content_type = ContentType.objects.get_for_model(Mouse)
        self.phone_content_type = ContentType.objects.get_for_model(Phone)
        self.speaker_content_type = ContentType.objects.get_for_model(Speaker)
        self.television_content_type = ContentType.objects.get_for_model(Television)
        
        # Wishlist instances
        self.wishlist_earbuds = Wishlist.objects.create(
            user=self.user,
            content_type=self.earbuds_content_type,
            object_id=self.earbuds.id
        )
        self.wishlist_keyboard = Wishlist.objects.create(
            user=self.user,
            content_type=self.keyboard_content_type,
            object_id=self.keyboard.id
        )
        self.wishlist_monitor = Wishlist.objects.create(
            user=self.user,
            content_type=self.monitor_content_type,
            object_id=self.monitor.id
        )
        self.wishlist_mouse = Wishlist.objects.create(
            user=self.user,
            content_type=self.mouse_content_type,
            object_id=self.mouse.id
        )
        self.wishlist_phone = Wishlist.objects.create(
            user=self.user,
            content_type=self.phone_content_type,
            object_id=self.phone.id
        )
        self.wishlist_speaker = Wishlist.objects.create(
            user=self.user,
            content_type=self.speaker_content_type,
            object_id=self.speaker.id
        )
        self.wishlist_television = Wishlist.objects.create(
            user=self.user,
            content_type=self.television_content_type,
            object_id=self.television.id
        )
    
    def test_add_wishlist(self):
        self.client.force_authenticate(user=self.user)
        new_earbuds = Earbuds.objects.create(
            name='new Earbuds',
            price=100.00,
            review_date='2023-06-21',
            wireless=True,
            battery_life=10.5,
            active_noise_cancellation=True
        )
        response = self.client.post(
            reverse('wishlist-list'),
            {
                "product_category": "earbuds",
                "object_id": new_earbuds.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Wishlist.objects.filter(user=self.user, object_id=self.earbuds.id).exists())
    
    def test_get_wishlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('wishlist-list'),
        )
        
        wishlist_items = Wishlist.objects.filter(user = self.user).order_by('-datetime')
        serializer = WishlistSerializer(wishlist_items, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)
    
    def test_delete_wishlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('wishlist-detail', args=[self.wishlist_television.id])
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Wishlist.objects.filter(id=self.wishlist_television.id).exists())
        
            
    # Incorrect Tests
    def test_unauthenticated_add(self):
        response = self.client.post(
            reverse('wishlist-list'),
            {
                "product_category": "earbuds",
                "object_id": self.earbuds.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_invalid_category_add(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('wishlist-list'),
            {
                "product_category": "bob",
                "object_id": self.earbuds.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid product category"})
        
    def test_invalid_product_id_add(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('wishlist-list'),
            {
                "product_category": "earbuds",
                "object_id": 6000
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Product not found"})
    
    def test_repeated_item_add(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(
            reverse('wishlist-list'),
            {
                "product_category": "earbuds",
                "object_id": self.earbuds.id
            }
        )
        
        response = self.client.post(
            reverse('wishlist-list'),
            {
                "product_category": "earbuds",
                "object_id": self.earbuds.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data, {'error': 'Item already exists in your wishlist'})
    
    def test_unauthenticated_get(self):
        response = self.client.get(
            reverse('wishlist-list')
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthenticated_delete(self):
        response = self.client.delete(
            reverse('wishlist-detail', args=[self.wishlist_television.id]),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthorised_delete(self):
        self.client.force_authenticate(user=self.alt_user)
        response = self.client.delete(
            reverse('wishlist-detail', args=[self.wishlist_television.id]),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_invalid_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('wishlist-detail', args=[6000])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
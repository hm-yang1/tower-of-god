from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from ..models.earbuds import Earbuds, EarbudSerializer
from ..models.keyboard import Keyboard, KeyboardSerializer
from ..models.laptop import Laptop, LaptopSerializer
from ..models.monitor import Monitor, MonitorSerializer
from ..models.mouse import Mouse, MouseSerializer
from ..models.phone import Phone, PhoneSerializer
from ..models.speaker import Speaker, SpeakerSerializer
from ..models.television import Television, TelevisionSerializer

class ComparisonViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_earbuds = Earbuds.objects.create(
            name='test Earbuds',
            price=100.00,
            review_date='2023-06-21',
            wireless=True,
            battery_life=10.5,
            active_noise_cancellation=True
        )
        self.test_keyboard = Keyboard.objects.create(
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
            
    def test_get_earbuds(self):
        q = 'a'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
                'category': 'earphone'
            }
        )
        
        products = Earbuds.objects.filter(name__icontains=q)
        serializer = EarbudSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_keyboards(self):
        q = 't'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
                'category': 'keyboard'
            }
        )
        
        products = Keyboard.objects.filter(name__icontains=q)
        serializer = KeyboardSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_keyboards(self):
        q = 't'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
                'category': 'laptop'
            }
        )
        
        products = Laptop.objects.filter(name__icontains=q)
        serializer = LaptopSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_monitors(self):
        q = 't'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
                'category': 'monitor'
            }
        )
        
        products = Monitor.objects.filter(name__icontains=q)
        serializer = MonitorSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mice(self):
        q = 't'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
                'category': 'mouse'
            }
        )
        
        products = Mouse.objects.filter(name__icontains=q)
        serializer = MouseSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_phones(self):
        q = 't'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
                'category': 'phone'
            }
        )
        
        products = Phone.objects.filter(name__icontains=q)
        serializer = PhoneSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_speakers(self):
        q = 't'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
                'category': 'speaker'
            }
        )
        
        products = Speaker.objects.filter(name__icontains=q)
        serializer = SpeakerSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_televisions(self):
        q = 't'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
                'category': 'television'
            }
        )
        
        products = Television.objects.filter(name__icontains=q)
        serializer = TelevisionSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ########## Incorrect Tests ##########
    def test_no_category(self):
        q='t'
        response = self.client.get(
            reverse('compare-list'), 
            {
                'q': q,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_no_search(self):
        response = self.client.get(
            reverse('compare-list'), 
            {
                'category': 'television'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

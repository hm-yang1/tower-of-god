from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from ..models.earbuds import Earbuds, EarbudSerializer
from ..models.keyboard import Keyboard, KeyboardSerializer
from ..models.laptop import Laptop, LaptopSerializer
from ..models.monitor import Monitor, MonitorSerializer
from ..models.mouse import Mouse, MouseSerializer
from ..models.phone import Phone, PhoneSerializer
from ..models.speaker import Speaker, SpeakerSerializer
from ..models.television import Television, TelevisionSerializer

class ProductViewSetTests(APITestCase):
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
        
    ################ Correct Tests ################
        
    # Earbuds tests
    
    def test_get_earbuds(self):
        q = 'ear test'
        response = self.client.get(reverse('product-list'), {'q': q})
        
        vector = SearchVector('name', 'brand', 'pros', weight = 'A')
        vector += SearchVector('description', weight = 'C') 
        vector += Earbuds.get_vectors()
        
        products = Earbuds.objects.annotate(rank = SearchRank(
            vector, 
            SearchQuery(q),
            normalization = 4,
        )).order_by("-rank")
        serializer = EarbudSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_earbuds_with_ordering(self):
        q = 'earbuds'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': 'review_date',
            }
        )
        products = Earbuds.objects.order_by('review_date')
        serializer = EarbudSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_earbuds_with_filters(self):
        q = 'earbuds'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'wireless': True,
            }
        )
        products = Earbuds.objects.all().filter(wireless = True)
        serializer = EarbudSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Keyboard Tests
    
    def test_get_keyboards(self):
        q = 'keyboard test'
        response = self.client.get(reverse('product-list'), {'q': q})
        
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Keyboard.get_vectors()
        
        products = Keyboard.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = KeyboardSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_keyboards_with_ordering(self):
        q = 'keyboard'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': 'review_date',
            }
        )
        products = Keyboard.objects.order_by('review_date')
        serializer = KeyboardSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_keyboards_with_filters(self):
        q = 'keyboard'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'wireless': True,
            }
        )
        products = Keyboard.objects.filter(wireless=True)
        serializer = KeyboardSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # Laptop Tests
    
    def test_get_laptops(self):
        q = 'laptop test'
        response = self.client.get(reverse('product-list'), {'q': q})
        
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Laptop.get_vectors()
        
        products = Laptop.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = LaptopSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_laptops_with_ordering(self):
        q = 'laptop'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': 'review_date',
            }
        )
        products = Laptop.objects.order_by('review_date')
        serializer = LaptopSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_keyboards_with_filters(self):
        q = 'laptop'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'wireless': True,
            }
        )
        products = Laptop.objects.filter(weight=2.2)
        serializer = LaptopSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Monitor tests

    def test_get_monitors(self):
        q = 'monitor test'
        response = self.client.get(reverse('product-list'), {'q': q})
        
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Monitor.get_vectors()
        
        products = Monitor.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = MonitorSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_monitors_with_ordering(self):
        q = 'monitor'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': 'review_date',
            }
        )
        products = Monitor.objects.order_by('review_date')
        serializer = MonitorSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_monitors_with_filters(self):
        q = 'monitor'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'screen_size': 27,
            }
        )
        products = Monitor.objects.filter(screen_size=27)
        serializer = MonitorSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Mouse tests

    def test_get_mice(self):
        q = 'mouse test'
        response = self.client.get(reverse('product-list'), {'q': q})
        
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Mouse.get_vectors()
        
        products = Mouse.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = MouseSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mice_with_ordering(self):
        q = 'mouse'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': '-price',
            }
        )
        products = Mouse.objects.order_by('-price')
        serializer = MouseSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mice_with_filters(self):
        q = 'mouse'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'wireless': True,
            }
        )
        products = Mouse.objects.filter(wireless=True)
        serializer = MouseSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Phone tests
    
    def test_get_phones(self):
        q = 'phone test'
        response = self.client.get(reverse('product-list'), {'q': q})
        
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Phone.get_vectors()
        
        products = Phone.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = PhoneSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_phones_with_ordering(self):
        q = 'phone'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': '-price',
            }
        )
        products = Phone.objects.order_by('-price')
        serializer = PhoneSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_phones_with_filters(self):
        q = 'phone'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'os_version': 'Android 12',
            }
        )
        products = Phone.objects.filter(os_version='Android 12')
        serializer = PhoneSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # Speakers test

    def test_get_speakers(self):
        q = 'speaker test'
        response = self.client.get(reverse('product-list'), {'q': q})
        
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Speaker.get_vectors()
        
        products = Speaker.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = SpeakerSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_speakers_with_ordering(self):
        q = 'speaker'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': 'price',
            }
        )
        products = Speaker.objects.order_by('price')
        serializer = SpeakerSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_speakers_with_filters(self):
        q = 'speaker'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'portable': True,
            }
        )
        products = Speaker.objects.filter(portable=True)
        serializer = SpeakerSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Television test

    def test_get_televisions(self):
        q = 'television test'
        response = self.client.get(reverse('product-list'), {'q': q})
        
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Television.get_vectors()
        
        products = Television.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = TelevisionSerializer(products, many=True)
        
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_televisions_with_ordering(self):
        q = 'television'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': '-screen_size',
            }
        )
        products = Television.objects.order_by('-screen_size')
        serializer = TelevisionSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_televisions_with_filters(self):
        q = 'television'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'panel_type': 'OLED',
            }
        )
        products = Television.objects.filter(panel_type='OLED')
        serializer = TelevisionSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    ################ Incorrect Tests ################
    def test_no_search(self):
        response = self.client.get(reverse('product-list'),)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # No errors for invalid ordering or filtering fields
    # Want api to always return some result, so returns to queryset as usual
    def test_incorrect_ordering(self):
        q = 'television'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'ordering': 'wireless',
            }
        )
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Television.get_vectors()
        
        products = Television.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = TelevisionSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_televisions_with_filters(self):
        q = 'television'
        response = self.client.get(
            reverse('product-list'), 
            {
                'q': q,
                'bob': 'really bob',
            }
        )
        vector = SearchVector('name', 'brand', 'pros', weight='A')
        vector += SearchVector('description', weight='C') 
        vector += Television.get_vectors()
        
        products = Television.objects.annotate(rank=SearchRank(
            vector, 
            SearchQuery(q),
            normalization=4,
        )).order_by("-rank")
        serializer = TelevisionSerializer(products, many=True)
        self.assertEqual(response.data.get('results').get('products'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

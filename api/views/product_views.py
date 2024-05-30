from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models.product import Product
from ..models.earbuds import Earbuds
from ..models.headphones import Headphones
from ..models.keyboard import Keyboard
from ..models.laptop import Laptop
from ..models.mouse import Mouse
from ..models.phone import Phone
from ..serial.product_serializers import (
    EarbudSerializer, 
    HeadphoneSerializer, 
    KeyboardSerializer, 
    LaptopSerializer, 
    MouseSerializer, 
    PhoneSerializer,
)

# Views for products
# Done with view sets to abstract common logic such as the search and filter fields
class ProductViewSet(ReadOnlyModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend]
    
    # Once fill in product info, extend and override in child views
    filterset_fields = ['brand']
    search_fields = ['name', 'brand', 'pros']
    
    def get_queryset(self):
        queryset = self.queryset
        return queryset

class EarbudsViewSet(ProductViewSet):
    queryset = Earbuds.objects.all()
    serializer_class = EarbudSerializer

class HeadphonesViewSet(ProductViewSet):
    queryset = Headphones.objects.all()
    serializer_class = HeadphoneSerializer

class KeyboardViewSet(ProductViewSet):
    queryset = Keyboard.objects.all()
    serializer_class = KeyboardSerializer

class LaptopViewSet(ProductViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer

class MouseViewSet(ProductViewSet):
    queryset = Mouse.objects.all()
    serializer_class = MouseSerializer

class PhoneViewSet(ProductViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
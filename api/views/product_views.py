from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rapidfuzz import process, fuzz, utils
from ..models.product import Product
from ..models.earbuds import Earbuds
from ..models.headphones import Headphones
from ..models.keyboard import Keyboard
from ..models.laptop import Laptop
from ..models.mouse import Mouse
from ..models.phone import Phone
from ..serial.product_serializers import (
    EarbudSerializer, 
    KeyboardSerializer, 
    LaptopSerializer, 
    MouseSerializer, 
    PhoneSerializer,
)

# Viewset for all products
class ProductViewSet(ReadOnlyModelViewSet):
    # Categories of products
    # placed here for convience, not sure if this is the most correct place to put this
    categories = {
            'earphones': [Earbuds, EarbudSerializer, []],
            'keyboard': [Keyboard, KeyboardSerializer, []],
            'laptop': [Laptop, LaptopSerializer, []],
            'mouse': [Mouse, MouseSerializer, []],
            'phone': [Phone, PhoneSerializer, []]
        }
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    filter_backends = [SearchFilter, DjangoFilterBackend]
    
    # After determining category, extend filter fields
    filterset_fields = ['brand', 'MSRP', 'release_date']
        
    # Determines catergory through fuzzy search. Performs full text search in the product fields
    def get_queryset(self):
        # Get search query from http request
        search_string = str(self.request.query_params.get('q', None))
        print(search_string)
        
        # Fuzzy search to determine category
        choices = list(self.categories.keys())
        
        # Scorers set to default ratio for now
        print(process.extractOne(search_string, choices, scorer=fuzz.ratio, processor= utils.default_process))
        category = process.extractOne(search_string, choices, scorer=fuzz.ratio, processor= utils.default_process)[0]
        
        # Remove category from search_string
        words = search_string.split()
        closest_match = process.extractOne(category, words, scorer=fuzz.ratio)[0]
        words.remove(closest_match)
        search_string = ' '.join(words)
        
        # doing setup after determining category
        cat_info = self.categories.get(category)
        model = cat_info[0]
        self.serializer_class = cat_info[1]
        self.filterset_fields.extend(cat_info[2])
        
        # Full text search
        print(search_string)
        query = SearchQuery(search_string)
        
        # Vectors determine fields to search for and weight of each field
        vector = SearchVector('name', 'brand', 'pros', weight = 'A')
        vector += SearchVector('description', weight = "C") 
        
        # Full text SearchRank with SearchQeury and SearchVectors
        queryset = model.objects.annotate(rank = SearchRank(vector, query)).order_by("rank")
        return queryset
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Count, F
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rapidfuzz import process, fuzz, utils
from ..models.earbuds import Earbuds, EarbudSerializer
from ..models.keyboard import Keyboard, KeyboardSerializer
from ..models.laptop import Laptop, LaptopSerializer
from ..models.monitor import Monitor, MonitorSerializer
from ..models.mouse import Mouse, MouseSerializer
from ..models.phone import Phone, PhoneSerializer
from ..models.speaker import Speaker, SpeakerSerializer
from ..models.television import Television, TelevisionSerializer

# Viewset for comparison page
# Really similar to product views, just without the fuzzy search and filtering the fields
# To get list of products of specific category most similar in name to search query, so user can add to comparison

class ComparisonViewSet(ReadOnlyModelViewSet):
    # Categories of products
    # placed here for convience, not sure if this is the most correct place to put this
    categories = {
        'earphone': [Earbuds, EarbudSerializer],
        'keyboard': [Keyboard, KeyboardSerializer],
        'laptop': [Laptop, LaptopSerializer],
        'monitor': [Monitor, MonitorSerializer],
        'mouse': [Mouse, MouseSerializer],
        'phone': [Phone, PhoneSerializer],
        'speaker': [Speaker, SpeakerSerializer],
        'television': [Television, TelevisionSerializer],
    }
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    filter_backends = [SearchFilter]
        
    def get_queryset(self):
        # Get cateogry from http request
        category_string = str(self.request.query_params.get('category', None))
        print(category_string)
        cat_info = self.categories.get(category_string)
        model = cat_info[0]
        self.serializer_class = cat_info[1]
        
        # Get search_string from http request
        search_string = str(self.request.query_params.get('q', None))
        print(search_string)
        
        # Search for product name.
        query = SearchQuery(search_string)
        
        # Only one search vector, name of product
        vector = SearchVector('name')
        
        # Full text SearchRank with SearchQeury and SearchVectors
        queryset = model.objects.annotate(rank = SearchRank(
            vector, 
            query,
        )).order_by("-rank")
        return queryset
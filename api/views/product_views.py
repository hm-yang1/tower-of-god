from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Count, F
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
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

# Viewset to query all products
class ProductViewSet(ReadOnlyModelViewSet):
    # Categories of products
    # placed here for convience, not sure if this is the most correct place to put this
    categories = {
        'earbuds': [Earbuds, EarbudSerializer],
        'headphone':[Earbuds, EarbudSerializer],
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
    
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    
    # After determining category, extend filter fields
    filterset_fields = ['brand', 'price', 'review_date']
    
    # Ordering fields, extend after determining category
    ordering_fields = ['price', 'review_date']
        
    # Determines catergory through fuzzy search. Performs full text search in the product fields
    def get_queryset(self):
        # Reset filterset_fields
        self.reset()
        
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
        closest_match = process.extractOne(category, words, scorer=fuzz.token_ratio)[0]
        words.remove(closest_match)
        search_string = ' '.join(words)
        
        # doing setup after determining category
        cat_info = self.categories.get(category)
        model = cat_info[0]
        self.serializer_class = cat_info[1]
        
        # Extend filterset_fields
        self.filterset_fields = self.filterset_fields + model.get_filters()
        print(self.filterset_fields)
        
        # Extend odering_fields
        self.ordering_fields = self.ordering_fields + model.get_orders()
        print(self.ordering_fields)
        
        # Full text search
        query = SearchQuery(search_string)
        
        # Vectors determine fields to search for and weight of each field
        vector = SearchVector('name', 'brand', 'pros', weight = 'A')
        vector += SearchVector('description', weight = 'C') 
        
        # Add vectors specific to each product category
        vector += model.get_vectors()
        
        # Full text SearchRank with SearchQeury and SearchVectors
        queryset = model.objects.annotate(rank = SearchRank(
            vector, 
            query,
            normalization = 4,
        )).order_by("-rank")
                
        # Additional weights with no. of reviews and reddit sentiment. Eg.
        
        # queryset = queryset.annotate(
        #     final_rank=F('search_rank') * 0.3 + F('num_reviews') * 0.7
        # ).order_by('-final_rank')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply ordering
        ordering = request.query_params.get('ordering', 'id')  # Default ordering by 'id'
        queryset = queryset.order_by(ordering)
        
        # Manually limit the queryset to at most 20 items
        limited_queryset = queryset[:20]
        
        page = self.paginate_queryset(limited_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(limited_queryset, many=True)
        return Response(serializer.data)
    
    def reset(self):
        self.filterset_fields = ['brand', 'price', 'review_date']
        self.ordering_fields = ['price', 'review_date']
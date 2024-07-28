from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Count, F, Value, IntegerField
from django.db.models.functions import Coalesce
from django.db.models.expressions import Func
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rapidfuzz import process, fuzz, utils
from ..category import Category
from ..models.earbuds import Earbuds, EarbudSerializer
from ..models.keyboard import Keyboard, KeyboardSerializer
from ..models.laptop import Laptop, LaptopSerializer
from ..models.monitor import Monitor, MonitorSerializer
from ..models.mouse import Mouse, MouseSerializer
from ..models.phone import Phone, PhoneSerializer
from ..models.speaker import Speaker, SpeakerSerializer
from ..models.television import Television, TelevisionSerializer

# Custom ordering filter to always sort null values to the bottom
class NullsAlwaysLastOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        print('Entered custom ordering')
        ordering = self.get_ordering(request, queryset, view)
        
        if ordering:
            f_ordering = []
            for o in ordering:
                if not o:
                    continue
                if o[0] == '-':
                    f_ordering.append(F(o[1:]).desc(nulls_last=True))
                else:
                    f_ordering.append(F(o).asc(nulls_last=True))
            return queryset.order_by(*f_ordering)
        
        return queryset

# Viewset to query all products
class ProductViewSet(ReadOnlyModelViewSet):
    # Categories of products
    categories = Category.get_categories()
    categories.update({
        'earbuds': [Earbuds, EarbudSerializer],
        'tv': [Television, TelevisionSerializer],
    })
    
    
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    
    # After determining category, extend filter fields
    filterset_fields = {}
    
    # Ordering fields, extend after determining category
    ordering_fields = []
        
    # Determines catergory through fuzzy search. Performs full text search in the product fields
    def get_queryset(self):
        # Reset filterset_fields
        self.reset()
        
        # Get search query from http request
        search_string = str(self.request.query_params.get('q', None))
        print('Search string: ' + search_string)
        
        if not search_string or search_string=='None':
            # Empty search strign defaults to mouse
            search_string = "mouse"

        category_string = str(self.request.query_params.get('category', ''))

        # if the category params is given, use that, else do fuzzy search for category
        if category_string:
            category = category_string
        else:
            # Fuzzy search to determine category
            choices = list(self.categories.keys())
            
            # Scorers set to default ratio for now
            print(process.extractOne(search_string, choices, scorer=fuzz.token_set_ratio, processor= utils.default_process))
            category = process.extractOne(search_string, choices, scorer=fuzz.token_set_ratio, processor= utils.default_process)[0]
                
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
        self.filterset_fields.update(model.get_filters())
        print(self.filterset_fields)
        
        # Extend odering_fields
        self.ordering_fields = model.get_orders()
        print(self.ordering_fields)
        
        # Full text search
        query = SearchQuery(search_string)
        
        # Vectors determine fields to search for and weight of each field
        vector = SearchVector('name', 'brand', 'pros', weight = 'A')
        vector += SearchVector('description', weight = 'C') 
        
        # Add vectors specific to each product category
        vector += model.get_vectors()
        
        # Full text SearchRank with SearchQeury and SearchVectors
        # Also added weights for num_reviews and score, score will be for later
        queryset = model.objects.annotate(
            rank=SearchRank(vector, query, normalization=4),
            num_reviews=Coalesce(Func(F('reviews'), function='jsonb_array_length', output_field=IntegerField()), Value(0)),
            score_weight=Coalesce(F('score'), Value(0))
        ).annotate(
            weighted_rank=F('rank') + F('num_reviews') * 0.1 + F('score_weight') * 0.1
        ).order_by('-weighted_rank')
        return queryset
    
    # Override list method for custom additional information in the response
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        model = queryset.model
        
        # Info for filter fields
        filter_info = model.get_filters()
        
        # Additional info for unique filter fields
        unique_filter_info = {}
        unique_filter_fields = model.get_specific_filters()
        for field in unique_filter_fields:
            values = list(model.objects.values_list(field, flat=True).distinct())
            unique_filter_info[str(field)] = values
        
        # Info about ordering fields
        order_fields = model.get_orders()
        
        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            # Add aggregated data to response
            data = {
                'filters': filter_info,
                'unique_filters': unique_filter_info,
                'orders': order_fields,
                'products': serializer.data,
            }
            filter_info = {}
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)

        # If no pagination
        data = {
            'filters': filter_info,
            'orders': order_fields,
            'products': serializer.data,
        }
        filter_info = {}
        return Response(data, status=status.HTTP_200_OK)
    
    def reset(self):
        self.filterset_fields = {}
        self.ordering_fields = ['price', 'review_date']

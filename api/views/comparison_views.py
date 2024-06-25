from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Count, F
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
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
        
        # Raise exception if no cat_info
        if not cat_info:
            raise ValidationError(f"Category '{category_string}' not found.")
        
        model = cat_info[0]
        self.serializer_class = cat_info[1]
        
        # Get search_string from http request
        search_string = str(self.request.query_params.get('q', None))
        print(search_string)
        
        queryset = model.objects.all()
        
        if search_string:
            queryset = model.objects.filter(name__icontains=search_string)
            
            print(str(queryset))
            return queryset
        
        return queryset
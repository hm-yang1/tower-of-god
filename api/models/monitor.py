from django.db import models
from django.db.models.functions import Cast
from django.contrib.postgres.search import SearchVector
from . import Product
from rest_framework import serializers

class Monitor(Product):
    screen_size = models.IntegerField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=50)
    refresh_rate = models.IntegerField(null=True, blank=True)
    panel_type = models.CharField(null=True, max_length=20)
    
    # Additional search vectors
    @classmethod
    def get_vectors(cls):
        vector = SearchVector('panel_type', 'screen_resolution', weight='A')
        vector += SearchVector(Cast('screen_size', models.CharField()), weight='A')
        return vector
    
    # Additional filter fields
    @classmethod
    def get_filters(cls):
        result = super().get_filters()
        filter_fields = {
            'screen_size': ['exact', 'gte', 'lte'],
            'screen_resolution': ['exact'],
            'refresh_rate': ['exact', 'gte', 'lte'],
            'panel_type': ['exact', 'icontains'],
        }
        result.update(filter_fields)
        return result
    
    # Get filter fields with unique results
    @classmethod
    def get_specific_filters(cls):
        result = super().get_specific_filters()
        filter_fields = [
            'panel_type'
        ]
        
        result.extend(filter_fields)
        return result
    
    # Get ordering fields
    @classmethod
    def get_orders(cls):
        result = super().get_orders()
        order_fields = [
            'screen_size',
            'refresh_rate',
            'screen_resolution',
        ]
        result.extend(order_fields)
        return result
    
    def combine(self, product):
        super().combine(product)
        
        for field in self._meta.get_fields():
            value_self = getattr(self, field.name)
            value_product = getattr(product, field.name)
            if value_self is None:
                setattr(self, field.name, value_product)
        
        return self
    
    def get_category_display(self):
        return 'monitor'

    def add_screen_size(self, screen_size: int):
        self.screen_size = screen_size
    
    def add_screen_resolution(self, width:int, height:int):
        self.screen_resolution = str(width) + ' x ' + str(height)
        
    def add_refresh_rate(self, rate: int):
        self.refresh_rate = rate
    
    def add_panel_type(self, panel_type: str):
        self.panel_type = panel_type
        
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + 'Size: ' + str(self.screen_size)
        string += '\n' + 'Resolution: ' + str(self.screen_resolution)
        string += '\n' + 'Refresh rate: ' + str(self.refresh_rate)
        string += '\n' + 'Type: ' + str(self.panel_type)
        return string
    
class MonitorSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Monitor
        fields = '__all__'
from django.db import models
from django.db.models.functions import Cast
from django.contrib.postgres.search import SearchVector
from . import Product
from rest_framework import serializers

class Phone(Product):
    # Model fields
    battery_life = models.JSONField(default=list, blank=True)
    os_version = models.CharField(null=True, max_length=50)
    size = models.IntegerField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=50)
    processor = models.CharField(null=True, max_length=50)
    
    # Additional search vectors
    @classmethod
    def get_vectors(cls):
        vector = SearchVector('battery_life', 'screen_resolution', 'processor', 'os_version', weight='A')
        vector += SearchVector(Cast('size', models.CharField()), weight='A')
        return vector
    
    # Additional filter fields
    @classmethod
    def get_filters(cls):
        return [
            'battery_life',
            'os_version',
            'size',
            'screen_resolution',
            'processor',
        ]
        
    # Additional ordering fields
    @classmethod
    def get_orders(cls):
        return [
            'screen_size',
            'screen_resolution'
        ]
    
    def combine(self, product):
        super().combine(product)
        
        self.battery_life.extend(product.battery_life)
        
        for field in self._meta.get_fields():
            value_self = getattr(self, field.name)
            value_product = getattr(product, field.name)
            if value_self is None:
                setattr(self, field.name, value_product)
        return self
    
    def get_category_display(self):
        return 'phone'

    def add_battery(self, battery: float, website: str, direct:bool = False):
        if direct:
            self.battery_life.append(website)
            return
        self.battery_life.append(str(battery) + ' hrs (' + website +')')
    
    def add_os(self, os: str):
        self.os_version = os
    
    def add_screen_size(self, size: float):
        self.size = size
    
    def add_screen_resolution(self, width:int, height:int):
        self.screen_resolution = str(width) + ' x ' + str(height)
    
    def add_processor(self, processor: str):
        self.processor = processor
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + str(self.battery_life)
        string += '\n' + str(self.size)
        string += '\n' + str(self.screen_resolution)
        string += '\n' + str(self.processor)
        return string
        
class PhoneSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Phone
        fields = '__all__'
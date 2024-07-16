from django.db import models
from django.db.models.functions import Cast
from django.contrib.postgres.search import SearchVector
from . import Product
from rest_framework import serializers

class Laptop(Product):
    # Model fields
    battery_life = models.JSONField(default=list, blank=True)
    weight = models.FloatField(null=True, blank=True)
    screen_size = models.FloatField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=100)
    processor = models.CharField(null=True, max_length=100)
    os_version = models.CharField(null=True, max_length=100)
    
    # Additional search vectors
    @classmethod
    def get_vectors(cls):
        vector = SearchVector('battery_life', 'screen_resolution', 'processor', 'os_version', weight='A')
        vector += SearchVector(Cast('screen_size', models.CharField()), weight='A')
        return vector
    
    # Additional filter fields
    @classmethod
    def get_filters(cls):
        result = super().get_filters()
        filter_fields = {
            'weight': ['exact', 'gte', 'lte'],
            'screen_size': ['exact', 'gte', 'lte'],
            'screen_resolution': ['exact'],
            'processor': ['exact', 'icontains'],
            'os_version': ['exact', 'icontains'],
        }
        result.update(filter_fields)
        return result
    
    # Get filter fields with unique results
    @classmethod
    def get_specific_filters(cls):
        result = super().get_specific_filters()
        filter_fields = [
            'processor',
            'os_version',
        ]
        
        result.extend(filter_fields)
        return result
    
    # Get ordering fields
    @classmethod
    def get_orders(cls):
        result = super().get_orders()
        order_fields = [
            'weight',
            'screen_size',
            'screen_resolution'
        ]
        result.extend(order_fields)
        return result
    
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
        return 'laptop'
    
    def add_price(self, price: float):
        if self.price: return
        if price and price < 300:
            self.price = price
    
    def add_battery(self, battery: float, website: str, direct:bool = False):
        if direct:
            self.battery_life.append(website)
            return
        self.battery_life.append(str(battery) + ' hrs (' + website +')')
    
    def add_weight(self, weight: float, pounds: bool):
        if self.weight is not None:
            return
        if pounds:
            self.weight = round(weight/2.205, 2)
        else:
            if weight > 100:
                self.weight = weight/100
            else:
                self.weight = weight
    
    def add_screen_size(self, screen_size: float):
        self.screen_size = screen_size
    
    def add_screen_resolution(self, width:int, height:int):
        self.screen_resolution = str(width) + ' x ' + str(height)
    
    def add_processor(self, processor: str):
        self.processor = processor
    
    def add_os(self, os: str):
        self.os_version = os
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + str(self.battery_life)
        string += '\n' + str(self.weight)
        string += '\n' + str(self.screen_size)
        string += '\n' + str(self.screen_resolution)
        string += '\n' + str(self.processor)
        
        return string
    
class LaptopSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Laptop
        fields = '__all__'
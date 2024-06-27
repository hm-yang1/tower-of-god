import math
from django.db import models
from django.db.models import Case, When, Value
from django.db.models.functions import Cast
from . import Product
from rest_framework import serializers
from django.contrib.postgres.search import SearchVector

class Keyboard(Product):
    # Model fields
    wireless = models.BooleanField(null=True, )
    size = models.IntegerField(null=True, blank=True)
    key_switches = models.CharField(null=True, max_length=50)
    
    # Get additional search vectors
    @classmethod
    def get_vectors(cls):
        # cast bool fields to char
        vector = SearchVector('key_switches', weight = 'A')
        vector = SearchVector(
            Case(
                When(wireless = True, then=Value('wireless')),
                When(wireless = False, then=Value('wired')),
                output_field=models.CharField()
            ), weight='A'
        )
        vector += SearchVector(Cast('size', models.CharField()), weight='A')
        return vector
    
    # Additional filter fields
    @classmethod
    def get_filters(cls):
        result = super().get_filters()
        filter_fields = {
            'wireless': ['exact'],
            'size': ['exact', 'gte', 'lte'],
            'key_switches': ['exact', 'icontains'],
        }
        result.update(filter_fields)
        return result
    
    # Additional ordering fields
    @classmethod
    def get_orders(cls):
        return [
            'size'
        ]
        
    def combine(self, product):
        super().combine(product)
        
        for field in self._meta.get_fields():
            value_self = getattr(self, field.name)
            value_product = getattr(product, field.name)
            if value_self is None:
                setattr(self, field.name, value_product)
        
        return self
    
    def get_category_display(self):
        return 'keyboard'

    def add_wireless(self, wireless: bool):
        self.wireless = wireless
    
    def add_size(self, size: int):
        if size > 100:
            self.size = 100
            return
        
        self.size = math.ceil(size/10) * 10
    
    def add_switches(self, key_switches: str):
        self.key_switches = key_switches
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + str(self.wireless)
        string += '\n' + str(self.size)
        string += '\n' + str(self.key_switches)
        return string

class KeyboardSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Keyboard
        fields = '__all__'
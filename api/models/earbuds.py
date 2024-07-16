from django.db import models
from django.db.models import Case, When, Value
from django.db.models.functions import Cast
from django.contrib.postgres.search import SearchVector
from . import Product
from rest_framework import serializers

class Earbuds(Product):
    # Model fields
    earphone_type = models.CharField(default='earbuds', blank=True, max_length=20)
    wireless = models.BooleanField(null=True, blank=True,)
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    active_noise_cancellation = models.BooleanField(null=True, blank=True)
    
    # Get additional search vectors for earbuds
    @classmethod
    def get_vectors(cls):
        # cast bool fields to char
        vector = SearchVector('earphone_type', weight = 'A')
        vector += SearchVector(
            Case(
                When(wireless = True, then=Value('wireless')),
                When(wireless = False, then=Value('wired')),
                output_field=models.CharField()
            ), weight='A'
        )
        vector += SearchVector(
            Case(
                When(active_noise_cancellation=True, then=Value('noise cancelling')),
                output_field=models.CharField()
            ), weight='A'
        )
        vector += SearchVector(Cast('battery_life', models.CharField()), weight='A')
        return vector
    
    # Additional filter fields
    @classmethod
    def get_filters(cls):
        result = super().get_filters()
        
        filter_fields = {
            'earphone_type': ['exact'],
            'wireless': ['exact'],
            'battery_life': ['exact', 'gte', 'lte'],
            'active_noise_cancellation': ['exact'],
        }
        result.update(filter_fields)
        return result
        
    # Get filter fields with unique results
    @classmethod
    def get_specific_filters(cls):
        result = super().get_specific_filters()
        filter_fields = [
            'earphone_type',
            'wireless',
            'active_noise_cancellation',
        ]
        
        result.extend(filter_fields)
        return result
    
    # Get ordering fields
    @classmethod
    def get_orders(cls):
        result = super().get_orders()
        order_fields = [
            'battery_life'
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
        
    # No point creating new column, just adding this to every serialized product
    def get_category_display(self):
        return 'earphones'
    
    def add_type(self, earbuds: bool):
        if earbuds: 
            self.earphone_type = 'earbuds'
        else: 
            self.earphone_type = 'headphones'
    
    def add_wireless(self, wireless: bool):
        self.wireless = wireless
    
    def add_battery(self, battery_life: float):
        if not self.wireless: return
        if self.battery_life is not None and battery_life > self.battery_life:
            return
        self.battery_life = battery_life
        
    def add_anc(self, anc: bool):
        self.active_noise_cancellation = anc
        
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + 'Type: ' + self.earphone_type
        string += '\n' + 'Wireless: ' + str(self.wireless)
        string += '\n' + 'Battery life: ' + str(self.battery_life)
        string += '\n' + 'ANC: '  + str(self.active_noise_cancellation)
        return string

class EarbudSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display', read_only=True)
    class Meta:
        model = Earbuds
        fields = '__all__'
    

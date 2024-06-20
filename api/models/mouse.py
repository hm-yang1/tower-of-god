from django.db import models
from django.db.models import Case, When, Value
from django.db.models.functions import Cast
from django.contrib.postgres.search import SearchVector
from . import Product
from rest_framework import serializers

class Mouse(Product):
    # Model fields
    wireless = models.BooleanField(null=True)    
    buttons_count = models.IntegerField(null=True)
    dpi = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    
    # Additional search vectors
    @classmethod
    def get_vectors(cls):
        vector = SearchVector(
            Case(
                When(wireless = True, then=Value('wireless')),
                When(wireless = False, then=Value('wired')),
                output_field=models.CharField()
            ), weight='A'
        )
        vector += SearchVector(Cast('buttons_count', models.CharField()), weight='A')
        vector += SearchVector(Cast('dpi', models.CharField()), weight='A')
        vector += SearchVector(Cast('weight', models.CharField()), weight='A')
        return vector
    
    # Additional filter fields
    @classmethod
    def get_filters(cls):
        return [
            'wireless',
            'buttons_count',
            'dpi',
            'weight'
        ]
        
    # Additional ordering fields
    @classmethod
    def get_orders(cls):
        return [
            'buttons_count',
            'dpi',
            'weight',
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
        return 'mouse'
    
    def add_wireless(self, wireless: bool):
        self.wireless = wireless
        
    def add_buttons(self, buttons: int):
        if self.buttons_count is not None:
            return
        self.buttons_count = buttons
    
    def add_dpi(self, dpi: int):
        if self.dpi is not None:
            return
        self.dpi = dpi
        
    def add_weight(self, weight: float, ounces:bool=False, pounds:bool=False):
        if self.weight is not None:
            return
        if ounces:
            self.weight = weight * 28.35
        elif pounds:
            self.weight = weight * 453.6
        else:
            self.weight = weight
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + str(self.wireless)
        string += '\n' + str(self.buttons_count)
        string += '\n' + str(self.dpi)
        string += '\n' + str(self.weight)
        return string
    

class MouseSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Mouse
        fields = '__all__'


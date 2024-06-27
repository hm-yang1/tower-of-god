from django.db import models
from django.db.models import Case, When, Value
from django.contrib.postgres.search import SearchVector
from . import Product
from rest_framework import serializers

class Speaker(Product):
    portable = models.BooleanField(null=True, blank=True)
    bluetooth = models.BooleanField(null=True, blank=True)
    wifi = models.BooleanField(null=True, blank=True)
    speakerphone = models.BooleanField(null=True, blank=True)
    
    # Get additional search vectors for earbuds
    @classmethod
    def get_vectors(cls):
        # cast bool fields to char
        vector = SearchVector(
            Case(
                When(bluetooth = True, then=Value('wireless')),
                When(bluetooth = False, then=Value('wired')),
                output_field=models.CharField()
            ), weight='A'
        )
        vector += SearchVector(
            Case(
                When(wifi = True, then=Value('wireless')),
                When(wifi = False, then=Value('wired')),
                output_field=models.CharField()
            ), weight='A'
        )
        vector += SearchVector(
            Case(
                When(portable = True, then=Value('portable')),
                output_field=models.CharField()
            ), weight='A'
        )
        vector += SearchVector(
            Case(
                When(speakerphone=True, then=Value('speakerphone')),
                output_field=models.CharField()
            ), weight='A'
        )
        return vector
    
    # Additional filter fields
    @classmethod
    def get_filters(cls):
        result = super().get_filters()
        filter_fields = {
            'portable': ['exact'],
            'bluetooth': ['exact'],
            'wifi': ['exact'],
            'speakerphone': ['exact'],
        }
        result.update(filter_fields)
        return result
    
    # Get filter fields with specific results
    @classmethod
    def get_specific_filters(cls):
        result = super().get_specific_filters()
        filter_fields = [
            'portable',
            'bluetooth',
            'wifi',
            'speakerphone'
        ]
        
        result.extend(filter_fields)
        return result
    
    # Additional ordering fields
    @classmethod
    def get_orders(cls):
        return [
            
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
        return 'speaker'
    
    def add_portable(self, portable: bool):
        self.portable = portable
    
    def add_bluetooth(self, bluetooth: bool):
        self.bluetooth = bluetooth
    
    def add_wifi(self, wifi: bool):
        self.wifi = wifi
    
    def add_speakerphone(self, speakerphone: bool):
        self.speakerphone = speakerphone
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + 'Portable: ' + str(self.portable)
        string += '\n' + 'Bluetooth: ' + str(self.bluetooth)
        string += '\n' + 'Wifi: ' + str(self.wifi)
        string += '\n' + 'Speakerphone: ' + str(self.speakerphone)
        return string

class SpeakerSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Speaker
        fields = '__all__'
from django.db import models
from . import Product
from rest_framework import serializers

class Mouse(Product):
    # Model fields
    wireless = models.BooleanField(null=True)    
    buttons_count = models.IntegerField(null=True)
    dpi = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    
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
        
    def add_weight(self, weight: float, ounces:bool):
        if self.weight is not None:
            return
        if ounces:
            self.weight = weight * 28.35
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


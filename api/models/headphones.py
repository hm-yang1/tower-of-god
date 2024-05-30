from django.db import models
from . import Product

class Headphones(Product):
    # Model fields
    wireless = models.BooleanField(null=True, )
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    active_noise_cancellation = models.BooleanField(null=True, )
    mic = models.BooleanField(null=True, )
    
    def __str__(self) -> str:
        return super().__str__()

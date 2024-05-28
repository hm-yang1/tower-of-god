from django.db import models
from product import Product

class Headphones(Product):
    # Model fields
    wireless = models.BooleanField()
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    active_noise_cancellation = models.BooleanField()
    mic = models.BooleanField()

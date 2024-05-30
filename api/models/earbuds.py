from django.db import models
from . import Product

class Earbuds(Product):
    # Model fields
    wireless = models.BooleanField(null=True, blank=True,)
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    active_noise_cancellation = models.BooleanField(null=True, blank=True)

from django.db import models
from product import Product

class Mouse(Product):
    # Model fields
    wireless = models.BooleanField()
    polling_rate = models.IntegerField()
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    buttons_count = models.IntegerField()
    dpi = models.IntegerField()
    weight = models.FloatField()
    ergonomics = models.CharField(max_length=100) 
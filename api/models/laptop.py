from django.db import models
from product import Product

class Laptop(Product):
    # Model fields
    battery_life = models.CharField(max_length=100, blank=True, null=True)
    weight = models.FloatField(blank=True)
    screen_size = models.FloatField(blank=True)
    screen_resolution = models.CharField(max_length=15)
    ports_available = models.JSONField(default=dict)
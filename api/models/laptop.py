from django.db import models
from . import Product

class Laptop(Product):
    # Model fields
    battery_life = models.CharField(null=True, max_length=100, blank=True)
    weight = models.FloatField(null=True, blank=True)
    screen_size = models.FloatField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=15)
    ports_available = models.JSONField(null=True, default=dict)
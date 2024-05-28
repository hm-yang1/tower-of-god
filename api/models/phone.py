from django.db import models
from product import Product

class Phone(Product):
    # Model fields
    battery_life = models.FloatField(blank=True)
    charging_speed = models.IntegerField(blank=True)
    os_version = models.CharField(max_length=50)
    software_updates_years = models.IntegerField(blank=True)
    size = models.IntegerField(blank=True)
    screen_resolution = models.CharField(max_length=15)
    screen_refresh_rate = models.IntegerField(blank=True)
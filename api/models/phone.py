from django.db import models
from . import Product

class Phone(Product):
    # Model fields
    battery_life = models.FloatField(null=True, blank=True)
    charging_speed = models.IntegerField(null=True, blank=True)
    os_version = models.CharField(null=True, max_length=50)
    software_updates_years = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=15)
    screen_refresh_rate = models.IntegerField(null=True, blank=True)
from django.db import models
from product import Product

class Keyboard(Product):
    # Model fields
    wireless = models.BooleanField()
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    size = models.CharField(max_length=10, choices=[('60%', '60%'), ('68%', '68%'), ('70%', '70%'), ('80%', '80%'), ('100%', '100%')])
    key_switches = models.CharField(max_length=50)

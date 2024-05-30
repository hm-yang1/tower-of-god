from django.db import models
from . import Product

class Mouse(Product):
    # Model fields
    wireless = models.BooleanField(null=True)
    polling_rate = models.IntegerField(null=True)
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    buttons_count = models.IntegerField(null=True)
    dpi = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    ergonomics = models.CharField(max_length=100, null=True) 
    
    def add_product(self):
        if not Mouse.objects.filter(name = self.name).exists():
            self.save()
            return
        
        database_input = Mouse.objects.filter.first()
        if self.reviews[0] in database_input.reviews:
            return
        
        database_input.add_review(self.reviews[0])
        database_input.add_description(self.description)
        database_input.pros.extend(self.pros)
        database_input.cons.extend(self.cons)
        database_input.save()
        return
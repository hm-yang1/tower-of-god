from django.db import models
from . import Product

# TO BE DELETED, MERGED MODEL WITH EARBUDS

class Headphones(Product):
    # Model fields
    wireless = models.BooleanField(null=True, )
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    active_noise_cancellation = models.BooleanField(null=True, )
    mic = models.BooleanField(null=True, )
    
    def add_wireless(self, wireless: bool):
        self.wireless = wireless
    
    def add_battery(self, battery_life: float):
        if not self.wireless: return
        if self.battery_life is not None and battery_life > self.battery_life:
            return
        self.battery_life = battery_life
        
    def add_anc(self, anc: bool):
        self.active_noise_cancellation = anc
        
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + str(self.wireless)
        string += '\n' + str(self.battery_life)
        string += '\n' + str(self.active_noise_cancellation)
        return string
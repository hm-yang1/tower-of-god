from django.db import models
from . import Product

class Earbuds(Product):
    # Model fields
    earphone_type = models.CharField(default='earbuds', blank=True, max_length=20)
    wireless = models.BooleanField(null=True, blank=True,)
    
    # Nullable field for battery life if wireless
    battery_life = models.FloatField(null=True, blank=True)
    
    active_noise_cancellation = models.BooleanField(null=True, blank=True)
    
    def add_type(self, earbuds: bool):
        if earbuds: 
            self.earphone_type = 'earbuds'
        else: 
            self.earphone_type = 'headphones'
    
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
        string += '\n' + 'Type: ' + self.earphone_type
        string += '\n' + str(self.wireless)
        string += '\n' + str(self.battery_life)
        string += '\n' + str(self.active_noise_cancellation)
        return string
    

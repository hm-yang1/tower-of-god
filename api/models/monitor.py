from django.db import models
from . import Product

class Monitor(Product):
    screen_size = models.IntegerField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=15)
    refresh_rate = models.IntegerField(null=True, blank=True)
    panel_type = models.CharField(null=True, max_length=20)
    
    def add_screen_size(self, screen_size: int):
        self.screen_size = screen_size
    
    def add_screen_resolution(self, width:int, height:int):
        self.screen_resolution = str(width) + ' x ' + str(height)
        
    def add_refresh_rate(self, rate: int):
        self.refresh_rate = rate
    
    def add_panel_type(self, panel_type: str):
        self.panel_type = panel_type
        
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + 'Size: ' + str(self.screen_size)
        string += '\n' + 'Resolution: ' + str(self.screen_resolution)
        string += '\n' + 'Refresh rate: ' + str(self.refresh_rate)
        string += '\n' + 'Type: ' + str(self.panel_type)
        return string
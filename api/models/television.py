from django.db import models
from . import Product

class Television(Product):
    screen_size = models.IntegerField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=15)
    panel_type = models.CharField(null=True, max_length=20)
    
    def add_screen_size(self, screen_size: int):
        self.screen_size = screen_size
    
    def add_screen_resolution(self, width:int, height:int):
        self.screen_resolution = str(width) + ' x ' + str(height)
    
    def add_panel_type(self, panel_type: str):
        self.panel_type = panel_type
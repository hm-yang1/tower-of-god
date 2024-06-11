from django.db import models
from . import Product

class Laptop(Product):
    # Model fields
    battery_life = models.JSONField(default=list, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    screen_size = models.FloatField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=15)
    processor = models.CharField(null=True, max_length=15)
    os_version = models.CharField(null=True, max_length=50)
    
    def add_battery(self, battery: float, website: str):
        self.battery_life.append(str(battery) + ' hrs (' + website +')')
    
    def add_weight(self, weight: float, pounds: bool):
        if self.weight is not None:
            return
        if pounds:
            self.weight = round(weight/2.205, 2)
        else:
            self.weight = weight
    
    def add_screen_size(self, screen_size: float):
        self.screen_size = screen_size
    
    def add_screen_resolution(self, width:int, height:int):
        self.screen_resolution = str(width) + ' x ' + str(height)
    
    def add_processor(self, processor: str):
        self.processor = processor
    
    def add_os(self, os: str):
        self.os_version = os
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + str(self.battery_life)
        string += '\n' + str(self.weight)
        string += '\n' + str(self.screen_size)
        string += '\n' + str(self.screen_resolution)
        string += '\n' + str(self.processor)
        
        return string
    
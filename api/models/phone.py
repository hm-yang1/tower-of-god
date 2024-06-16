from django.db import models
from . import Product

class Phone(Product):
    # Model fields
    battery_life = models.JSONField(default=list, null=True, blank=True)
    os_version = models.CharField(null=True, max_length=50)
    size = models.IntegerField(null=True, blank=True)
    screen_resolution = models.CharField(null=True, max_length=15)
    screen_refresh_rate = models.IntegerField(null=True, blank=True)
    processor = models.CharField(null=True, max_length=15)

    def add_battery(self, battery: float, website: str, direct:bool = False):
        if direct:
            self.battery_life.append(website)
            return
        self.battery_life.append(str(battery) + ' hrs (' + website +')')
    
    def add_os(self, os: str):
        self.os_version = os
    
    def add_screen_size(self, size: float):
        self.size = size
    
    def add_screen_resolution(self, width:int, height:int):
        self.screen_resolution = str(width) + ' x ' + str(height)
    
    def add_processor(self, processor: str):
        self.processor = processor
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + str(self.battery_life)
        string += '\n' + str(self.size)
        string += '\n' + str(self.screen_resolution)
        string += '\n' + str(self.processor)
        return string
        
from django.db import models
from . import Product

class Keyboard(Product):
    # Model fields
    wireless = models.BooleanField(null=True, )
    size = models.IntegerField(null=True, blank=True)
    key_switches = models.CharField(null=True, max_length=50)

    def add_wireless(self, wireless: bool):
        self.wireless = wireless
    
    def add_size(self, size: int):
        self.size = size
    
    def add_switches(self, key_switches: str):
        self.key_switches = key_switches
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + str(self.wireless)
        string += '\n' + str(self.size)
        string += '\n' + str(self.key_switches)
        return string
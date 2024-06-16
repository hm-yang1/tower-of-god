from django.db import models
from . import Product

class Speaker(Product):
    portable = models.BooleanField(null=True, blank=True)
    bluetooth = models.BooleanField(null=True, blank=True)
    wifi = models.BooleanField(null=True, blank=True)
    speakerphone = models.BooleanField(null=True, blank=True)
    
    def add_portable(self, portable: bool):
        self.portable = portable
    
    def add_bluetooth(self, bluetooth: bool):
        self.bluetooth = bluetooth
    
    def add_wifi(self, wifi: bool):
        self.wifi = wifi
    
    def add_speakerphone(self, speakerphone: bool):
        self.speakerphone = speakerphone
    
    def __str__(self) -> str:
        string = super().__str__()
        string += '\n' + 'Portable: ' + str(self.portable)
        string += '\n' + 'Bluetooth: ' + str(self.bluetooth)
        string += '\n' + 'Wifi: ' + str(self.wifi)
        string += '\n' + 'Speakerphone: ' + str(self.speakerphone)
        return string
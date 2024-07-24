from .models.earbuds import EarbudSerializer, Earbuds
from .models.keyboard import Keyboard, KeyboardSerializer
from .models.laptop import Laptop, LaptopSerializer
from .models.monitor import Monitor, MonitorSerializer
from .models.mouse import Mouse, MouseSerializer
from .models.phone import Phone, PhoneSerializer
from .models.speaker import Speaker, SpeakerSerializer
from .models.television import Television, TelevisionSerializer

# Class for centralised location of categories of products
class Category():
    categories = {
        'earphones': [Earbuds, EarbudSerializer],
        'keyboard': [Keyboard, KeyboardSerializer],
        'laptop': [Laptop, LaptopSerializer],
        'monitor': [Monitor, MonitorSerializer],
        'mouse': [Mouse, MouseSerializer],
        'phone': [Phone, PhoneSerializer],
        'speaker': [Speaker, SpeakerSerializer],
        'television': [Television, TelevisionSerializer],
    }
    
    @classmethod
    def get_categories(cls):
        return cls.categories
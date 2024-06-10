import os
import sys
import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
import api.models as model
from selenium import webdriver
from bisect import insort
from bisect import bisect_left

class Scrapper:
    # A parent class for all scrappers
    # set options for the webdriver and some helpful functions
    
    # Django models for the products. 
    # Scrapper will return lists of Django models
    categories = {
        'earbuds': model.Earbuds,
        'keyboard': model.Keyboard,
        'laptop': model.Laptop,
        'mouse': model.Mouse,
        'phone': model.Phone,
    }
        
    def __init__(self):
        self.firefox_options = webdriver.FirefoxOptions()
        self.firefox_options.add_argument("-headless")
        self.firefox_options.set_preference("browser.privatebrowsing.autostart", True)
        self.names: list[str]
    
    # *_name keeps track list of product names to prevent repeated scrapping of the same product
    def reset_names(self):
        self.names = []
        
    def insert_name(self, name: str):
        insort(self.names, name)
    
    def check_name(self, name: str) -> bool:
        i = bisect_left(self.names, name)
        return i != len(self.names) and self.names[i] == name
        
    def start(self, url: str = None) -> webdriver:
        driver = webdriver.Firefox(self.firefox_options)
        driver.set_window_size(1980, 1080)
        driver.get(url)
        # driver.implicitly_wait(1)
        return driver
    
    def end(self, webdriver:webdriver):
        webdriver.quit()

import os
import sys
import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
import api.models as model
from selenium import webdriver
from selenium.webdriver.common.by import By
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
        'television': model.Television,
        'monitor': model.Monitor,
        'speaker': model.Speaker,
    }
        
    def __init__(self):
        self.firefox_options = webdriver.FirefoxOptions()
        self.firefox_options.add_argument("-headless")
        self.firefox_options.set_preference("browser.privatebrowsing.autostart", True)
        self.names: list[str]
    
    def get_price(self, product):
        amazon_url = 'https://www.amazon.sg/s?k=' + product.name
        driver = self.start(amazon_url)
        
        # Need additional waiting cause amazon special, might block if too fast
        driver.implicitly_wait(5)
        
        # Get price of product
        search_results = driver.find_elements(By.CSS_SELECTOR, '[data-component-type="s-search-result"]')
        for search_result in search_results:
            # Check if sponsored post
            if len(search_result.find_elements(By.CLASS_NAME, 'puis-label-popover.puis-sponsored-label-text')) > 0: continue
            
            possible_prices = search_result.find_elements(By.CLASS_NAME, 'a-price-whole')
            if len(possible_prices) > 0: 
                price = possible_prices[0].text.replace(',','')
                product.add_price(float(price))
                break
        
        self.end(driver)
        return product
    
    # *_name keeps track list of product names to prevent repeated scrapping of the same product
    def reset_names(self):
        self.names = []
        
    def insert_name(self, name: str):
        insort(self.names, name)
    
    def check_name(self, name: str) -> bool:
        i = bisect_left(self.names, name)
        return i != len(self.names) and self.names[i] == name
    
    def filter(self, strings: list[str], include:bool=True):
        # Helper function to create filter to filter recommendation urls
        if include:
            return lambda x: any(string in x for string in strings)
        else:
            return lambda x: not any(string in x for string in strings)
        
    def start(self, url: str = None) -> webdriver:
        driver = webdriver.Firefox(self.firefox_options)
        driver.set_window_size(1920, 1080)
        driver.get(url)
        # driver.implicitly_wait(1)
        return driver
    
    def end(self, webdriver:webdriver):
        webdriver.quit()

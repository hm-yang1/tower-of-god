import os
import sys
import time
import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
import api.models as model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bisect import insort
from bisect import bisect_left
from urllib.parse import unquote

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
        if product.get_price():
            return product
        
        amazon_url = 'https://www.amazon.sg/s?k=' + product.get_name()
        driver = self.start(amazon_url)
        print(amazon_url)
        
        # Need additional waiting cause amazon special, might block if too fast
        driver.implicitly_wait(60)
        time.sleep(10)
        
        try:
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
        except NoSuchElementException as e:
            print(e)
            print(product)
        finally:        
            self.end(driver)
            return product
    
    def get_img_url(self, product):
        # If img_url exist, don't scrape
        if product.get_img_url():
            return product
        
        googe_img_url = 'https://www.google.com/search?q=' + '+'.join(product.name.split()) + '+official+product+image&udm=2'
        
        driver = self.start(googe_img_url)
        print(googe_img_url)
        try:
            # Need additional waiting cause google also special, might block if too fast
            driver.implicitly_wait(60)
            time.sleep(15)
            
            # Get img url
            img_wrapper = driver.find_element(By.XPATH, '//div[@jsname="dTDiAc"]')
            driver.implicitly_wait(60)
            img_wrapper.click()
            raw_img_url = img_wrapper.find_element(By.TAG_NAME, 'a').get_attribute('href')
            
            # Parsing image url
            encoded_img_url = raw_img_url.split('&imgurl=')[1].split('&')[0]
            
            # Decode url with urllib
            url = unquote(encoded_img_url)
            product.add_img_url(url)
        except NoSuchElementException as e:
            print(product)
            print(e)
        finally:
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
        return driver
    
    def end(self, webdriver:webdriver):
        webdriver.quit()

def main():
    scrapper = Scrapper()
    Product = scrapper.categories['monitor']
    product = Product(name='AOC Q27G3XMN')
    product = scrapper.get_img_url(product)
    print(str(product))
        
if __name__ == "__main__":
    main()
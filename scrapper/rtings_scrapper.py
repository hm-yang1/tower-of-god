import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from selenium.webdriver.common.by import By
from multiprocessing.pool import ThreadPool
from typing import Callable
from Scrapper import Scrapper
from api.models import Product

class rtings_scrapper(Scrapper):
    def __init__(self):
        super().__init__()
        self.website = 'https://www.rtings.com'
    
    def get_earbuds(self) -> list[Product]:
        url = 'https://www.rtings.com/headphones/reviews/best'
        products = self.get_products(url, lambda x: 'earbuds' in x)
        return products
    
    def get_headphones(self) -> list[Product]:
        url = 'https://www.rtings.com/headphones/reviews/best'
        products = self.get_products(url, lambda x: not('earbuds' or 'airpods') in x)
        return products
    
    def get_keyboards(self) -> list[Product]:
        url = 'https://www.rtings.com/keyboard/reviews/best'
        products = self.get_products(url, lambda x: True)
        return products
    
    def get_laptops(self) -> list[Product]:
        url = 'https://www.rtings.com/laptop/reviews/best'
        products = self.get_products(url, lambda x: True)
        return products
            
    def get_mice(self) -> list[Product]:
        url = 'https://www.rtings.com/mouse/reviews/best'
        products = self.get_products(url, lambda x: True)
        return products
        
    def get_monitors(self) -> list[Product]:
        url = 'https://www.rtings.com/monitor/reviews/best'
        products = self.get_products(url, lambda x: True)
        return products
    
    def get_television(self) -> list[Product]:
        url = 'https://www.rtings.com/tv/reviews/best'
        products = self.get_products(url, lambda x: True)
        return products
    
    def get_products(self, url:str, filter_func:Callable) -> list[Product]:
        # General get products function
        products = []
        self.reset_names()
        
        # Get all the recommendation urls fron the best * page
        recommendation_urls = list(
            filter(filter_func, self.parse_best_page(url))
        )
        print(recommendation_urls)

        # Go to each recommedation page and get the recommended products, runs concurrently
        results = ThreadPool().map(self.parse_recommendations, recommendation_urls)
        for result in results:
            products.extend(result) 
                  
        for product in products:
            print(product.__str__())
        
        return products
    
    def parse_best_page(self, url:str) -> list[str]:
        # Extract all urls on a best * page
        # * means random product. Eg. Mouse/Headphone/Etc
        driver = self.start(url)
        urls = []
        
        # Inner function to parse the tiles where links are located
        def parse_tiles(web_element) -> list[str]:
            # Given a web_element with many tiles, extract the urls
            urls = []
            tiles = web_element.find_elements(By.TAG_NAME, 'a')
            for tile in tiles:
                link = tile.get_attribute('href')
                urls.append(link)
            return urls
    
        # Get all the tiles on the best * page
        categories = driver.find_elements(By.CLASS_NAME, 'tiles-group')
        for category in categories:
            urls.extend(parse_tiles(category))
                
        self.end(driver)
        return urls
    
    def parse_recommendations(self, url:str) -> list[Product]:
        # driver go recommendation page
        # Wanted to add concurrency here but seems to crash local machine
        driver = self.start(url)
        recommendations = driver.find_elements(By.CLASS_NAME, 'recommendation_page-block')
        products = []
        for recommendation in recommendations:
            # Find and instantiate new product
            p_name = recommendation.find_element(By.CLASS_NAME, 'recommendation_page-block-name')
            name = p_name.text.split('\n')[0]
            
            # Check if product already exist
            if self.check_name(name):
                continue
            else: 
                self.insert_name(name)
            
            # Instantiate new product
            product = Product(name = name)
            
            # Get link of review
            p_url = p_name.find_element(By.TAG_NAME, 'a').get_attribute('href')
            product.add_review(p_url)
            
            # Get recommendation reasons
            summary_block = recommendation.find_element(By.CLASS_NAME, 'e-rich_content')
            summary = summary_block.find_elements(By.TAG_NAME, 'p')
            for paragraphs in summary:
                product.add_description(paragraphs.text)
            
            products.append(self.parse_review(product, p_url))
        
        self.end(driver)
        return products
    
    def parse_review(self, product:Product, url:str) -> Product:
        driver = self.start(url)
        
        # Get description of product
        texts = driver.find_element(By.CLASS_NAME, 'product_page-header').find_element(By.CLASS_NAME, 'e-rich_content').find_elements(By.TAG_NAME, 'p')
        for text in texts:
            product.add_description(text.text)
        
        # Get pros and cons
        sections = driver.find_elements(By.CLASS_NAME, 'usage_card-summary-body')
        for section in sections:
            pros_and_cons = section.find_elements(By.CLASS_NAME, 'product_page-summary-group')
            if len(pros_and_cons) < 2: continue
            pros = pros_and_cons[0].find_elements(By.TAG_NAME, 'li')
            cons = pros_and_cons[1].find_elements(By.TAG_NAME, 'li')
            for pro in pros:
                product.add_pros(pro.find_element(By.CLASS_NAME, 'e-rich_content').get_attribute('innerHTML'))
            for con in cons:
                product.add_cons(con.find_element(By.CLASS_NAME, 'e-rich_content').get_attribute('innerHTML'))
        # remove duplicates
        product.pros = list(set(product.pros)) #might not be the best way
        product.cons = list(set(product.cons))
        
        self.end(driver)
        return product

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    # settings.configure()
    scrapper = rtings_scrapper()
    # scrapper.get_earbuds()
    # scrapper.get_headphones()
    # scrapper.get_keyboards()
    # scrapper.get_mice()
    # scrapper.get_monitors()
    scrapper.get_laptops()
    # scrapper.get_television()
    
if __name__ == "__main__":
    main()
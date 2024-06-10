import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from multiprocessing.pool import ThreadPool
from rapidfuzz import fuzz
from random import sample
from Scrapper import Scrapper

class pcmag_scrapper(Scrapper):
    def __new__(cls):
        # Overriding default creation of new instance, no point for more than 1 instance
        if not hasattr(cls, 'instance'):
            cls.instance = super(pcmag_scrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.website = 'https://www.pcmag.com'
    
    def get_methods(self) -> list:
        # return list of methods to call to get data for various categories
        return [
            self.get_earbuds,
            self.get_keyboards,
            self.get_laptops,
            self.get_mice,
            self.get_phones,
            
            # self.get_monitors,
            # self.get_television,
        ]
    
    def get_earbuds(self) -> list:
        category = 'earbuds'
        url = 'https://www.pcmag.com/categories/headphones'
        products = self.get_products(category, url) 
        return products
    
    def get_keyboards(self) -> list:
        category = 'keyboard'
        url = 'https://www.pcmag.com/categories/keyboards'
        products = self.get_products(category, url)
        return products
    
    def get_laptops(self) -> list:
        category = 'laptop'
        url = 'https://www.pcmag.com/categories/laptops'
        products = self.get_products(category, url)
        return products
            
    def get_mice(self) -> list:
        category = 'mouse'
        url = 'https://www.pcmag.com/categories/computer-mice'
        products = self.get_products(category, url)
        return products
    
    def get_phones(self) -> list:
        category = 'phone'
        url = 'https://www.pcmag.com/categories/mobile-phones'
        products = self.get_products(category, url)
        return products
        
    def get_monitors(self) -> list:
        category = 'monitor'
        url = 'https://www.pcmag.com/categories/monitors'
        products = self.get_products(category, url)
        return products
    
    def get_television(self) -> list:
        category = 'television'
        url = 'https://www.pcmag.com/categories/tvs'
        products = self.get_products(category, url)
        return products
    
    def get_speakers(self) -> list:
        category = 'speaker'
        url = 'https://www.pcmag.com/categories/speakers'
        products = self.get_products(category, url)
        return products
    
    def get_products(self, category:str, url:str) -> list:
        # General get products function
        products = []
        self.reset_names()
        
        # Get all the recommendation urls fron the best * page
        recommendation_urls = self.parse_best_page(url)
        print(recommendation_urls)

        # Go to each recommedation page and get the recommended products, runs concurrently
        curried_parse_recommendation = lambda x: self.parse_recommendations(category, x)
        results = ThreadPool().map(curried_parse_recommendation, recommendation_urls)
        for result in results:
            products.extend(result) 
                  
        for product in products:
            print(product.__str__())
        
        return products
        
    def parse_best_page(self, url:str) -> list[str]:
        driver = self.start(url)
        urls = []
        
        url_elements = driver.find_element(By.ID, 'featured-picks').find_elements(By.TAG_NAME, 'a')
        for url_element in url_elements:
            urls.append(url_element.get_attribute('href'))
        
        self.end(driver)
        return urls
    
    def parse_recommendations(self, category:str, url:str) -> list:
        driver = self.start(url)
        products = []
        Product = self.categories[category]
        
        recommendations = driver.find_elements(By.XPATH, "//div[@data-parent-group='roundup-product-card']")
        for recommendation in recommendations:
            name = recommendation.find_element(By.TAG_NAME, 'h3').text
            
            # Check if product already scrapped
            if self.check_name(name):
                continue
            else:
                self.insert_name(name)
            
            # Instantiate new product
            product = Product(name = name)
            product.add_brand(name.split()[0])
            
            # Get recommendation reasons
            paragraphs = recommendation.find_elements(By.TAG_NAME, 'p')
            for paragraph in paragraphs:
                product.add_description(paragraph.text)
                
            # Get review url
            url = recommendation.find_element(By.CLASS_NAME, 'mt-2.inline-block.font-semibold.text-red-400.underline').get_attribute('href')
            product.add_review(url)
            
            products.append(self.parse_review(product, category, url))
            
        self.end(driver)
        return products
    
    def parse_review(self, product, category: str, url:str = None):
        driver = self.start(url)
        
        # Get summary
        summary = driver.find_element(By.CLASS_NAME, 'bottom-line.w-full.pt-6.text-base').text
        product.add_description(summary)
        
        # Get pros and cons
        pros_and_cons = driver.find_elements(By.XPATH, "//ul[@class='mb-8']")
        # Get pros
        pros = pros_and_cons[0].find_elements(By.TAG_NAME, 'li')
        for pro in pros:
            product.add_pros(pro.text)
        # Get cons
        cons = pros_and_cons[1].find_elements(By.TAG_NAME, 'li')
        for con in cons:
            product.add_cons(con.text)
            
        # Get description
        article = driver.find_element(By.ID, 'article')
        paragraphs = article.find_elements(By.TAG_NAME, 'p')
        
        # Articles kinda long, might consider randomly choosing paragraphs
        for paragraph in paragraphs[:-5]:
            product.add_description(paragraph.text)
        
        #TODO Add scraping for detailed information for specific category of product
        self.end(driver)
        return product

def main():
    scrapper = pcmag_scrapper()
    # scrapper.get_earbuds()
    # scrapper.get_keyboards()
    scrapper.get_laptops()
    # scrapper.get_mice()
    # scrapper.get_phones()
    
if __name__ == "__main__":
    main()
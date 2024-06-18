from math import prod
import re
from typing import Callable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from multiprocessing.pool import ThreadPool
from rapidfuzz import fuzz
from random import sample
from .Scrapper import Scrapper

class techradar_scrapper(Scrapper):
    # This website damn annoying, formatting for product specs not standardised
    def __new__(cls):
        # Overriding default creation of new instance, no point for more than 1 instance
        if not hasattr(cls, 'instance'):
            cls.instance = super(techradar_scrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.website = 'https://www.techradar.com'
        self.website_name = 'techradar.com'
    
    def get_methods(self) -> list:
        # return list of methods to call to get data for various categories
        return [
            [self.get_earbuds, self.categories['earbuds']],
            [self.get_laptops, self.categories['laptop']],
            [self.get_television, self.categories['television']],
            [self.get_phones, self.categories['phone']],
            [self.get_speakers, self.categories['speaker']]
        ]
    
    def get_earbuds(self) -> list:
        category = 'earbuds'
        url = 'https://www.techradar.com/audio/headphones/best'
        filter = self.filter([''])
        products = self.get_products(category, url, filter, 2) 
        return products
    
    def get_laptops(self) -> list:
        category = 'laptop'
        url = 'https://www.techradar.com/computing/laptops/best'
        filter = self.filter(['laptop'])
        products = self.get_products(category, url, filter, 2) 
        return products
    
    def get_phones(self) -> list:
        category = 'phone'
        url = 'https://www.techradar.com/phones/best'
        filter = self.filter(['phone'])
        products = self.get_products(category, url, filter, 1) 
        return products
    
    def get_television(self) -> list:
        category = 'television'
        url = 'https://www.techradar.com/televisions/best'
        filter = self.filter(['tv'])
        products = self.get_products(category, url, filter, 2) 
        return products
    
    def get_speakers(self) -> list:
        category = 'speaker'
        url = 'https://www.techradar.com/audio/best'
        filter = self.filter(['speaker'])
        products = self.get_products(category, url, filter, 2) 
        return products
    
    def get_tablets(self) -> list:
        category = 'tablet'
        url = 'https://www.techradar.com/tablets/best'
        filter = self.filter(['tablet'])
        products = self.get_products(category, url, filter, 2) 
        return products
    
    def get_mice(self) -> list:
        category = 'mouse'
        url = ''
        products = self.get_products(category, url) 
        return products
    
    def get_keyboards(self) -> list:
        category = 'earbuds'
        url = ''
        products = self.get_products(category, url) 
        return products
    
    def get_products(self, category:str, url:str, filter:Callable, page_limit:int) -> list:
        # General get products function
        products = []
        self.reset_names()
        
        # Get all the recommendation urls fron the best * page
        recommendation_urls = self.parse_best_page(url, filter, page_limit)
        print('techradar_scrapper: Got urls')
        
        # Go to each recommedation page and get the recommended products, runs concurrently
        curried_parse_recommendation = lambda x: self.parse_recommendations(category, x)
        pool = ThreadPool(6)
        results = pool.map(curried_parse_recommendation, recommendation_urls)
        for result in results:
            products.extend(result) 
        pool.close()
        
        print('techradar_scrapper: Finished getting products')

        return products
        
    def parse_best_page(self, url, fil:Callable, page_limit:int) -> list[str]:
        urls = []
        for i in range(1, page_limit + 1):
            curr_url = url + '/page/' + str(i)
            driver = self.start(curr_url)
            
            # Get recommendation links
            results = driver.find_element(By.CLASS_NAME, 'listingResults.best')
            link_elements = results.find_elements(By.CLASS_NAME, 'article-link')
            for link_element in link_elements:
                urls.append(link_element.get_attribute('href'))
            
            self.end(driver)
        
        return list(filter(fil, urls))
    
    def parse_recommendations(self, category:str, url:str) -> list:
        driver = self.start(url)
        products = []
        Product = self.categories[category]
        
        product_cards = driver.find_elements(By.CLASS_NAME, 'product.prog-buying-guide')
        for product_card in product_cards:            
            title = product_card.find_element(By.CLASS_NAME, 'product__title')
            name = title.text
            name = name[3:]
            
            # Check if product already scrapped
            if self.check_name(name):
                continue
            else:
                self.insert_name(name)
            
            # Instantiate new product
            product = Product(name = name)
            product.add_brand(name.split()[0])
            
            # If earphone, determine type
            if category == 'earbuds':
                subtitle = product_card.find_element(By.CLASS_NAME, '_hawk.subtitle').text
                product.add_type('earbud' in subtitle)
            
            # Get recommendation reasons
            paragraphs = driver.find_elements(locate_with(By.TAG_NAME, 'p').below(product_card))
            for paragraph in paragraphs[:5]:
                product.add_description(paragraph.text)
            
            # Get specs. Getting specs here instead of in review cause some reviews have missing specs tables
            specs = None
            try:
                specs = self.parse_specs_table(product_card)
            except Exception as e:
                print(e)
                print(name)
                print(url)
                continue
            
            # Get review url
            review_url_element = title.find_elements(By.TAG_NAME, 'a')
            if len(review_url_element) != 1: continue
            review_url = review_url_element[0].get_attribute('href')
            if review_url and review_url != url:
                product.add_review(review_url)
                products.append(self.parse_review(product, specs, category, review_url))

        self.end(driver)
        return products
    
    def parse_review(self, product, specs:dict, category: str, url:str = None):
        driver = self.start(url)
        
        try:
            # Get review date
            review_date = driver.find_element(By.TAG_NAME, 'time').text.split()
            day = int(review_date[0])
            year = int(review_date[2])
            month_map = {
                "January": 1, "February": 2, "March": 3, "April": 4,"May": 5, "June": 6,
                "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
            }
            month = int(month_map[review_date[1]])
            product.add_date(year, month, day)
            
            # Get verdict card
            verdict_card = driver.find_element(By.CLASS_NAME, 'pretty-verdict')
            # Get verdict
            verdict = verdict_card.find_element(By.CLASS_NAME, 'pretty-verdict__verdict').find_element(By.TAG_NAME, 'p')
            product.add_description(verdict.text)
            
            # Get pros
            pros = verdict_card.find_element(By.CLASS_NAME, 'pretty-verdict__pros').find_elements(By.TAG_NAME, 'li')
            for pro in pros:
                product.add_pros(pro.text[1:])
            # Get cons
            cons = verdict_card.find_element(By.CLASS_NAME, 'pretty-verdict__cons').find_elements(By.TAG_NAME, 'li')
            for con in cons:
                product.add_cons(con.text[1:])
                
            # Get description
            article = driver.find_element(By.ID, 'article-body')
            paragraphs = article.find_elements(By.TAG_NAME, 'p')
            
            # If have editors note, skip first 2 paragraphs
            if len(article.find_elements(By.ID, 'section-editor-s-note')) > 0:
                paragraphs = paragraphs[2:]
            
            # Articles kinda long, choosing first 5
            for paragraph in paragraphs[:10]:
                if len(paragraph.find_elements(By.TAG_NAME, 'strong')) > 0: continue
                product.add_description(paragraph.text)
            
            #Additional information for specific category of product
            match category:
                case 'earbuds':
                    product = self.parse_earbuds(product, specs)
                case 'laptop':
                    product = self.parse_laptop(product, specs)
                case 'phone':
                    product = self.parse_phone(product, specs)
                case 'television':
                    product = self.parse_television(product, specs)
                case 'speaker':
                    product = self.parse_speaker(product, specs)
                case 'tablet':
                    product = self.parse_tablet(product, specs)
        except Exception as e:
            print(url)
            print(e)
        finally:
            self.end(driver)
        
        return product
    
    def parse_earbuds(self, product, specs):
        # Get wireless and battery life
        if 'Battery life:' not in specs:
            product.add_wireless(False)
        else:
            battery = specs['Battery life:']
            if battery == 'N/A': 
                product.add_wireless(False)
                return product
            
            product.add_wireless(True)
            
            # Battery string complicated, need additional parsing
            # Basically get all numbers in string and get largest
            product.add_battery(max(map(float, re.findall(r'\d+\.\d+|\d+', battery))))
        
        # No way to consistently scrape anc from this website
        return product
    
    def parse_laptop(self, product, specs):
        # Get processor
        processor = None
        if 'Processor:' in specs:
            processor = specs['Processor:']
        if 'CPU:' in specs:
            processor = specs['CPU:']
        product.add_processor(processor)
        
        # Get screen size
        size = None
        if 'Screen:' in specs:
            size = specs['Screen:']
        if 'Screen size:' in specs:
            size = specs['Screen size:']
        if size:
            match_size = re.search(r'[-+]?\d*\.?\d+', size)
            if match_size:
                size = match_size.group()
                product.add_screen_size(float(size))
        
        # Get weight
        weight = None
        if 'Weight:' in specs:
            weight = specs['Weight:']
            match_weight = re.search(r'[-+]?\d*\.?\d+', weight)
            if match_weight:
                weight = match_weight.group()
            product.add_weight(float(weight), True)
        
        # Parsing battery life
        battery = None
        if 'Tested Battery Life (TechRadar test):' in specs:
            battery = specs['Tested Battery Life (TechRadar test):']
        if 'Battery life (TechRadar test):' in specs:
            battery = specs['Battery life (TechRadar test):']
        product.add_battery(0, battery, True)
        
        # No way to consistently scrape os and screen resolution
        return product
    
    def parse_phone(self, product, specs):
        product.add_os(specs['OS:'])
        product.add_processor(specs['CPU:'])
        
        screen_size_string = specs['Screen size:'].split('-')[0]
        product.add_screen_size(float(screen_size_string))
        
        # Parsing screen resolution
        resolution_string = specs['Resolution:'].split()
        if len(resolution_string) > 2:
            product.add_screen_resolution(
                int(resolution_string[0].replace(',','')), 
                int(resolution_string[2].replace(',',''))
            )
        
        # Parsing battery life
        product.add_battery(0, specs['Battery:'] + ' (' + self.website_name + ')', True)
        return product
    
    def parse_television(self, product, specs):
        # Get screen size
        size = None
        if 'Screen size:' in specs:
            product.add_screen_size(int(re.findall(r'\b\d+\b', specs['Screen size:'])[0]))
        
        # Get panel type
        panel = None
        if 'Panel Type:' in specs:
            panel = specs['Panel Type:']
        if 'Panel type:' in specs:
            panel = specs['Panel type:']
        if panel:
            product.add_panel_type(specs['Panel type:'])
        
        # Website tv resolution not standardised, too annoying to scrape
        return product
    
    def parse_speaker(self, product, specs):
        product.add_portable('Battery life:' in specs)
        
        connectivity = None
        if 'Connectivity:' in specs:
            connectivity = specs['Connectivity:']
        if 'Supported connectivity :' in specs:
            connectivity = specs['Supported connectivity :']
        if connectivity:
            product.add_bluetooth('Bluetooth' in connectivity)
            product.add_wifi('Wi-Fi' in connectivity)
        
        return product
    
    def parse_tablet(product, specs):
        pass
    
    def parse_specs_table(self, element) -> dict[str, str]:
        # Function to parse specs table in recommendation page
        specs_elements = element.find_element(By.CLASS_NAME, 'product-summary__container').find_elements(By.CLASS_NAME, 'spec__entry')
        specs = {}
        
        for specs_element in specs_elements:
            key = specs_element.find_element(By.CLASS_NAME, 'spec__name').text
            value = specs_element.find_element(By.CLASS_NAME, 'spec_value').text
            specs[key] = value
        
        return specs

def main():
    scrapper = techradar_scrapper()
    # url = 'https://www.techradar.com/audio/best'
    # filter = scrapper.filter(['speaker'])
    # recommendation_urls = scrapper.parse_best_page(url, filter, 2)
    # print(recommendation_urls)
    
    # url = 'https://www.techradar.com/news/audio/portable-audio/best-over-ear-headphones-1280342'
    # scrapper.reset_names()
    # products = scrapper.parse_recommendations('earbuds', url)
    # print(str(products))
    
    # scrapper.get_earbuds()
    # scrapper.get_laptops()
    # scrapper.get_phones()
    scrapper.get_television()
    # scrapper.get_speakers()
    
if __name__ == "__main__":
    main()
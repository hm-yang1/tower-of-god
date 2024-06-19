from functools import partial
from operator import is_not
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from rapidfuzz import fuzz
from random import sample
from .Scrapper import Scrapper

class notebookcheck_scrapper(Scrapper):
    def __new__(cls):
        # Overriding default creation of new instance, no point for more than 1 instance
        if not hasattr(cls, 'instance'):
            cls.instance = super(notebookcheck_scrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.website = 'https://www.notebookcheck.net/Laptop-Search.8223.0.html'
        self.website_name = 'notebookcheck.net'
    
    def get_methods(self) -> list:
        # return list of methods to call to get data for various categories
        return [
            [self.get_laptops, self.categories['laptop']],
            [self.get_phones, self.categories['phone']],
            
            # self.get_tablets,
        ]
    
    def get_laptops(self) -> list:
        return self.get_products('laptop', 88, 10)
    
    def get_phones(self) -> list:
        return self.get_products('phone', 85, 10)
    
    def get_tablets(self) -> list:
        return self.get_products('tablet', 85, 10)
    
    def get_products(self, category:str, percentage: int, age: int) -> list:
        # Construct search url, easier than working with old html form
        url = self.website + '?'
        
        # select category
        url += '&class='
        match category:
            case 'laptop':
                url += '-1'
            case 'phone':
                url += '10'
            case 'tablet':
                url += '9'
                
        # add min rating
        url += '&rating='
        url += str(percentage)
        
        # add age
        url += '&age='
        url += str(age)
        
        # no external reviews
        url += '&nbcReviews=1'
        # Order by rating
        url += '&orderby=1'
        
        # Uses search form to search for products
        driver = self.start(url)
        
        # Scrape search results
        urls = []
        review_table = driver.find_element(By.ID, 'search')
        link_elements = review_table.find_elements(By.PARTIAL_LINK_TEXT, 'review')
        for link_element in link_elements:
            urls.append(link_element.get_attribute('href'))
        print('notebookcheck_scrapper: Got urls')
        
        self.end(driver)
                
        # Concurrency for parse review
        # Keeps breaking for some god damn reason
        products = []
        curried_parse_review = lambda x: self.parse_review(category, x)
        pool = ThreadPool(6)
        results = pool.map(curried_parse_review, urls)
        products.extend(results)
        pool.close()

        # for url in urls:
        #     product = self.parse_review(category, url)
        #     products.append(product)
        
        products = list(filter(partial(is_not, None), products))
        print('notebookcheck_scrapper: Finished getting products')

        return products
            
    def parse_review(self, category, url):
        # Try except needed cause this website gives errors too frequently
        # Might be good practice to add to other scrapper
        driver = None
        product = None
        try: 
            driver = self.start(url)
            driver.implicitly_wait(5)
            
            # Get full article
            article = driver.find_element(By.ID, 'content')
            
            # Parse specs
            specs_whole = article.find_elements(By.CLASS_NAME, 'specs_whole')
            if not specs_whole: 
                print('No product. url: ' + url)
                self.end(driver)
                return product
            
            # Parse name
            name_string = specs_whole[0].find_element(By.CLASS_NAME, 'specs_header').text
            name = re.sub(r'\(.*?\)', '', name_string).strip()
            
            # Instantiate new product
            Product = self.categories[category]
            product = Product(name = name)
            product.add_brand(name.split()[0])
            product.add_review(url)
            
            # Get review date
            review_date_string = article.find_element(By.TAG_NAME, 'time').text
            review_date = review_date_string.split('/')
            day = int(review_date[1])
            month = int(review_date[0])
            year = int(review_date[2])
            product.add_date(year, month, day)
            
            # Parse rest of specs
            specs_elements = specs_whole[0].find_elements(By.CLASS_NAME, 'specs_element')
            specs = {}
            if specs_elements:
                for spec_element in specs_elements:
                    keys = spec_element.find_elements(By.CLASS_NAME, 'specs')
                    if len(keys) < 1: continue
                    key = keys[0]
                    value = spec_element.find_element(By.CLASS_NAME, 'specs_details')
                    
                    # Check if got link
                    links = value.find_elements(By.TAG_NAME, 'a')
                    if len(links) > 0:
                        specs[key.text] = links[0].text
                        continue
                    
                    specs[key.text] = value.text
            
            # Get pros and cons
            pros_and_cons = article.find_elements(By.CLASS_NAME, 'ttcl_55.csc-default.csc-space-before-5.csc-space-after-15')[-1]

            # Get pros
            pros = pros_and_cons.find_element(By.CLASS_NAME, 'pc_element.pc_element_pro').find_elements(By.CLASS_NAME, 'pc_tr')
            for pro in pros:
                product.add_pros(pro.text[2:])
            
            # Get cons
            cons = pros_and_cons.find_element(By.CLASS_NAME, 'pc_element.pc_element_contra').find_elements(By.CLASS_NAME, 'pc_tr')
            for con in cons:
                product.add_cons(con.text[2:])
            
            # Get description
            verdict = article.find_elements(By.CLASS_NAME, 'ttcl_0.csc-default')
            paragraphs = verdict[0].find_elements(By.TAG_NAME, 'p') + verdict[-6].find_elements(By.TAG_NAME, 'p')
            for paragraph in paragraphs:
                product.add_description(paragraph.text)
            
            # Skip addition parsing if no specs_elements
            if not specs_elements: return product
            
            # Additional parsing for specific category
            match category:
                case 'laptop':
                    product = self.parse_laptop(product, specs, article)
                case 'phone':
                    product = self.parse_phone(product, specs, article)
                case 'tablet':
                    product = self.parse_tablet(product, specs, article)
        
        except Exception as e:
            print(e)
            print(url)
        
        finally:
            if driver is not None:
                driver = self.end(driver)
            product.remove_duplicates()
            return product
        
    def parse_laptop(self, product, specs, article):
        product = self.parse_phone(product, specs, article)
        product.add_weight(float(specs['Weight'].split()[0]), False)
        # product.add_os()
        return product
        
    def parse_phone(self, product, specs, article):        
        # Parse battery
        battery_elements = article.find_element(By.CLASS_NAME, 'barcharts').find_elements(By.CLASS_NAME, 'runtime')
        if battery_elements:
            if len(battery_elements) > 1:
                product.add_battery(float(re.findall(r'(\d+)h', battery_elements[1].text)[0]), self.website_name)
            else:
                product.add_battery(float(re.findall(r'(\d+)h', battery_elements[0].text)[0]), self.website_name)
        
        # Parsing display
        display_string = specs['Display'].split(',')
        product.add_screen_size(float(re.findall(r'\b\d+\.\d+\b', display_string[0])[0]))
        
        resolution_string = display_string[1].split()
        product.add_screen_resolution(int(resolution_string[0]), int(resolution_string[2]))
        
        # Parse processor
        product.add_processor(specs['Processor'])    
        
        return product
    
    def parse_tablet(self, product, specs, article):
        product = self.parse_laptop(product, specs, article)
        return product

def main():
    scrapper = notebookcheck_scrapper()
    scrapper.get_phones()
    # scrapper.get_laptops()
    # scrapper.parse_review('phone', 'https://www.notebookcheck.net/Google-Pixel-8-smartphone-review-Compact-and-with-7-years-of-updates.768436.0.html')
    
    # product = scrapper.parse_review('laptop', 'https://www.notebookcheck.net/Apple-MacBook-Pro-16-2023-M3-Max-Review-M3-Max-challenges-HX-CPUs-from-AMD-Intel.766414.0.html')
    # print(str(product))
    
    # # Models not implemented yet
    # # scrapper.get_tablets()
    
if __name__ == "__main__":
    main()
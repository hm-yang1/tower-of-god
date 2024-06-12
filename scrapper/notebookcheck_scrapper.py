import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from multiprocessing.pool import ThreadPool
from rapidfuzz import fuzz
from random import sample
from Scrapper import Scrapper

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
            self.get_laptops,
            self.get_phones,
            
            # self.get_tablets,
        ]
    
    def get_laptops(self) -> list:
        return self.get_products('laptop', 90, 10)
    
    def get_phones(self) -> list:
        return self.get_products('phone', 88, 10)
    
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
        print(str(urls))
        print(len(urls))
        
        # Concurrency for parse review
        products = []
        curried_parse_review = lambda x: self.parse_review(category, x)
        pool = ThreadPool()
        results = pool.map(curried_parse_review, urls)
        products.extend(results)
        pool.close()

        # for url in urls:
        #     product = self.parse_review(category, url)
        #     products.append(product)
        
        return products
            
    def parse_review(self, category, url):
        driver = self.start(url)
        
        # Get full article
        article = driver.find_element(By.ID, 'content')
        
        print(url)
        
        # Parse specs
        specs_whole = article.find_elements(By.CLASS_NAME, 'specs_whole')
        if not specs_whole: 
            print('No product' + url)
            return None
        
        # Parse name
        name_string = specs_whole[0].find_element(By.CLASS_NAME, 'specs_header').text
        name = re.sub(r'\(.*?\)', '', name_string).strip()
        # Instantiate new product
        Product = self.categories[category]
        product = Product(name = name)
        product.add_brand(name.split()[0])
        product.add_review(url)
        
        # Parse rest of specs
        specs_elements = specs_whole.find_elements(By.CLASS_NAME, 'specs_element')
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
        
        # Get conclusion
        verdict = article.find_elements(locate_with(By.CLASS_NAME, 'ttcl_0.csc-default').below({By.CLASS_NAME: 'pc_whole.tx-nbc2fe-incontent-column'}))
        product.add_description(verdict.text)
        
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
        
        print(product.__str__())
        return product
        
    def parse_laptop(self, product, specs, article):
        product = self.parse_phone(product, specs, article)
        product.add_weight(specs['Weight'].split()[0], False)
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
        product.add_screen_size(re.findall(r'\b\d+\.\d+\b', display_string[0])[0])
        
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
    
    # Models not implemented yet
    # scrapper.get_tablets()
    
if __name__ == "__main__":
    main()
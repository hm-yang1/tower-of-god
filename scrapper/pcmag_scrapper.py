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
        self.website_name = 'pcmag.com'
    
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
            # self.get_speakers,
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
        pool = ThreadPool()
        results = pool.map(curried_parse_recommendation, recommendation_urls)
        for result in results:
            products.extend(result) 
        pool.close()
        
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
            
            # Get specs
            # Getting specs here instead of in review cause some reviews have missing specs tables
            specs = self.parse_specs_table(recommendation)
                
            # Get review url
            url = recommendation.find_element(By.CLASS_NAME, 'mt-2.inline-block.font-semibold.text-red-400.underline').get_attribute('href')
            product.add_review(url)
            
            products.append(self.parse_review(product, specs, category, url))
            
        self.end(driver)
        return products
    
    def parse_review(self, product, specs:dict, category: str, url:str = None):
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
        
        # Articles kinda long, choosing 1st and last paragraphs
        product.add_description(paragraphs[0].text)
        product.add_description(paragraphs[-6].text)
        
        #Additional information for specific category of product
        match category:
            case 'earbuds':
                product = self.parse_earbuds(product, specs)
            case 'keyboard':
                product = self.parse_keyboard(product, specs)
            case 'laptop':
                product = self.parse_laptop(product, specs)
            case 'mouse':
                product = self.parse_mouse(product, specs)
            case 'phone':
                product = self.parse_phone(product, specs)
        
        self.end(driver)
        return product
    
    def parse_earbuds(self, product, specs:dict):
        product.add_type(specs['Type'] == 'In-Canal')
        product.add_wireless(specs['Wireless'] == 'True')
        product.add_anc(specs['Active Noise Cancellation'] == 'True')
        
        # Unable to scrape battery
        return product
    
    def parse_keyboard(self, product, specs:dict):
        # Parsing wireless
        wireless_string = specs['Interface']
        wireless_keywords = ['Wireless', 'Bluetooth']            
        product.add_wireless(any(keyword in wireless_string for keyword in wireless_keywords))
        
        product.add_size(int(specs['Number of Keys']))
        product.add_switches(specs['Key Switch Type'])
        return product
    
    def parse_laptop(self, product, specs:dict):
        product.add_processor(specs['Processor'])
        product.add_screen_size(float(specs['Screen Size'].split()[0]))
        product.add_weight(float(specs['Weight'].split()[0]), True)
        product.add_os(specs['Operating System'])
        
        # Parsing screen resolution
        resolution_string = specs['Native Display Resolution'].split()
        product.add_screen_resolution(int(resolution_string[0].replace(',', '')), int(resolution_string[2].replace(',','')))
        
        # Parsing battery life
        battery_string = specs['Tested Battery Life (Hours:Minutes)'].split(':')
        product.add_battery(float(battery_string[0]) + float(battery_string[1])/60, self.website_name)
        return product
    
    def parse_mouse(self, product, specs:dict):
        # Parsing wireless
        wireless_string = specs['Interface']
        wireless_keywords = ['Wireless', 'Bluetooth']            
        product.add_wireless(any(keyword in wireless_string for keyword in wireless_keywords))
        
        product.add_buttons(int(specs['Number of Buttons']))
        product.add_dpi(int(specs['Sensor Maximum Resolution'].split()[0]))
        product.add_weight(float(specs['Weight'].split()[0]), True)
        return product
    
    def parse_phone(self, product, specs:dict):
        product.add_os(specs['Operating System'])
        product.add_processor(specs['CPU'])
        product.add_screen_size(specs['Screen Size'])
        
        # Parsing screen resolution
        resolution_string = specs['Screen Resolution'].split()
        product.add_screen_resolution(
            int(resolution_string[0].replace(',','')), 
            int(resolution_string[2].replace(',',''))
        )
        
        # Parsing battery life
        product.add_battery(
            float(re.findall(r'\d+', specs['Battery Life (As Tested)'])[0]),
            self.website_name
        )
        return product
    
    def parse_specs_table(self, element) -> dict[str, str]:
        # Expand specs table
        element.find_element(By.LINK_TEXT, 'ALL SPECS').click()
        
        # Get specs table
        table = element.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        
        # format specs table into a dict
        specs = {}
        for row in rows:
            key_and_value = row.find_elements(By.TAG_NAME, 'td')
            if len(key_and_value) < 2: continue
            key = key_and_value[0].text
            value = key_and_value[1].text
            if value:
                specs[key] = value
                continue
            
            # Check if thing is check mark or cross
            check = len(key_and_value[1].find_elements(By.XPATH, "//svg[@data-icon='check']")) > 0
            if check:
                specs[key] = 'True'
            else:
                specs[key] = 'False'
        return specs

def main():
    scrapper = pcmag_scrapper()
    # url = 'https://www.pcmag.com/picks/the-best-trackball-mice'
    # driver = scrapper.start(url)
    # element = driver.find_element(By.XPATH, "//div[@data-parent-group='roundup-product-card']")
    # scrapper.parse_specs_table(element)
    # scrapper.get_earbuds()
    # scrapper.get_keyboards()
    # scrapper.get_laptops()
    # scrapper.get_mice()
    scrapper.get_phones()
    
    # Models not implemented yet
    # scrapper.get_television()
    # scrapper.get_monitors()
    # scrapper.get_speakers()
    
if __name__ == "__main__":
    main()
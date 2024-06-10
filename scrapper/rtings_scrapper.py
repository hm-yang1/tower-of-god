# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# django.setup()
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from multiprocessing.pool import ThreadPool
from rapidfuzz import fuzz
from typing import Callable
from Scrapper import Scrapper

class rtings_scrapper(Scrapper):
    def __new__(cls):
        # Overriding default creation of new instance, no point for more than 1 instance
        if not hasattr(cls, 'instance'):
            cls.instance = super(rtings_scrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.website = 'https://www.rtings.com/search?q='
    
    def get_methods(self) -> list:
        # return list of methods to call to get data for various categories
        return [
            self.get_earbuds,
            self.get_headphones,
            self.get_keyboards,
            self.get_laptops,
            self.get_mice,
            
            # self.get_monitors,
            # self.get_television,
        ]
    
    def get_earbuds(self) -> list:
        category = 'earbuds'
        url = 'https://www.rtings.com/headphones/reviews/best'
        products = self.get_products(
            category, 
            url, 
            lambda x: 'earbuds' in x or 'airpods' in x or 'neckband' in x)
        return products
    
    def get_headphones(self) -> list:
        category = 'headphones'
        url = 'https://www.rtings.com/headphones/reviews/best'
        products = self.get_products(
            category, 
            url, 
            lambda x: not('earbuds' in x) and not('airpods' in x)  and not('neckband'in x))
        return products
    
    def get_keyboards(self) -> list:
        category = 'keyboard'
        url = 'https://www.rtings.com/keyboard/reviews/best'
        products = self.get_products(category, url, lambda x: True)
        return products
    
    def get_laptops(self) -> list:
        category = 'laptop'
        url = 'https://www.rtings.com/laptop/reviews/best'
        products = self.get_products(category, url, lambda x: True)
        return products
            
    def get_mice(self) -> list:
        category = 'mouse'
        url = 'https://www.rtings.com/mouse/reviews/best'
        products = self.get_products(category, url, lambda x: True)
        return products
        
    def get_monitors(self) -> list:
        category = 'monitor'
        url = 'https://www.rtings.com/monitor/reviews/best'
        products = self.get_products(category, url, lambda x: True)
        return products
    
    def get_television(self) -> list:
        category = 'television'
        url = 'https://www.rtings.com/tv/reviews/best'
        products = self.get_products(category, url, lambda x: True)
        return products
    
    def get_products(self, category:str, url:str, filter_func:Callable) -> list:
        # General get products function
        products = []
        self.reset_names()
        
        # Get all the recommendation urls fron the best * page
        recommendation_urls = list(
            filter(filter_func, self.parse_best_page(url))
        )
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
    
    def parse_recommendations(self, category:str, url:str) -> list:
        # driver go recommendation page
        # Wanted to add concurrency here but seems to crash local machine
        driver = self.start(url)
        recommendations = driver.find_elements(By.CLASS_NAME, 'recommendation_page-block')
        products = []
        Product = self.categories[category]
        
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
            product.add_brand(name.split(' ')[0])
            
            # Get link of review
            p_url = p_name.find_element(By.TAG_NAME, 'a').get_attribute('href')
            product.add_review(p_url)
            
            # Get recommendation reasons
            summary_block = recommendation.find_element(By.CLASS_NAME, 'e-rich_content')
            summary = summary_block.find_elements(By.TAG_NAME, 'p')
            for paragraphs in summary:
                product.add_description(paragraphs.text)
            
            products.append(self.parse_review(product, category, p_url))
        
        self.end(driver)
        return products
    
    def parse_review(self, product, category: str, url:str = None):
        # Allow url of review to be None, for use in other scrappers/Django commands
        # Search for review if url is None
        if url is None:
            temp_driver = self.start(self.website + product.name)
            url = temp_driver.find_element(By.CLASS_NAME, 'searchbar_results-name').get_attribute('href')
            
            # Go to review page
            temp_driver.get(url)
            temp_driver.implicitly_wait(1)
            
            # Checks if is the correct review
            fuzz_score = fuzz.ratio(product.name, temp_driver.find_element(By.CLASS_NAME, 'e-page_title-primary').text)
            self.end(temp_driver)
            if fuzz_score < 90:
                return product
        
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

        # Add additional info according to category of product
        match category:
            case 'earbuds':
                product = self.parse_earbuds(product, driver)
            case 'headphones':
                product = self.parse_headphones(product, driver)
            case 'keyboard':
                product = self.parse_keyboard(product, driver)
            case 'laptop':
                product = self.parse_laptop(product, driver)
            case 'mouse':
                product = self.parse_mouse(product, driver)
        
        self.end(driver)
        return product
    
    # Below are methods that parse additionaly info for each category
    def parse_earbuds(self, product, driver):
        # Get wireless
        bluetooth_card = driver.find_element(locate_with(By.CLASS_NAME, 'test_group-header').below({By.ID: 'test_1941'}))
        bluetooth_score = float(bluetooth_card.find_element(By.CLASS_NAME, 'e-score_box-value').text)
        
        dongle_card = driver.find_element(locate_with(By.CLASS_NAME, 'test_group-header').below({By.ID: 'test_3290'}))
        dongle_score = float(dongle_card.find_element(By.CLASS_NAME, 'e-score_box-value').text)
        
        product.add_wireless(bluetooth_score>0 or dongle_score > 0)
        
        # Get battery life
        if product.wireless:
            battery_card = self.get_card(driver, '407')
            battery = battery_card.find_elements(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score')[3].text
            product.add_battery(float(battery.split()[0]))
        
        # Get ANC
        anc_card = self.get_card(driver, '348')
        anc = anc_card.find_element(By.CLASS_NAME, 'test_value.is-word').find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score').text
        product.add_anc(anc == 'Yes')
        
        return product
        
    def parse_headphones(self, product, driver):
        product = self.parse_earbuds(product, driver)
        return product
    
    def parse_keyboard(self, product, driver):
        # Get wireless
        wireless_card = driver.find_element(locate_with(By.CLASS_NAME, 'test_group-header').below({By.ID: 'test_3361'}))
        wireless_score = float(wireless_card.find_element(By.CLASS_NAME, 'e-score_box-value').text)
        product.add_wireless(wireless_score > 0)
        
        # Get size
        size_card = self.get_card(driver, '3424')
        size = size_card.find_element(By.CLASS_NAME, 'test_value.is-word').find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score').text
        match = re.search(r'\((\d+)%\)', size)
        if match:
            percentage = int(match.group(1))
            product.add_size(percentage)
            
        # Get switches
        switches_card = self.get_card(driver, '19295')
        if switches_card is not None:
            switches = switches_card.find_element(By.CLASS_NAME, 'test_value.is-word').find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score.ld-paywall').text
            product.add_switches(switches)
        
        return product
    
    def parse_laptop(self, product, driver):
        # Get battery life
        battery_card = self.get_card(driver, '6114')
        battery = battery_card.find_elements(By.CLASS_NAME, 'test_value.is-number')[1].find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score.ld-paywall').text
        product.add_battery(float(battery.split()[0]), 'rtings.com')
        
        # Get size and weight
        portability_card = self.get_card(driver, '5187')
        portability = portability_card.find_elements(By.CLASS_NAME, 'test_value.is-number')
        
        size = portability[0].find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score').text
        product.add_screen_size(float(size.replace('"', '')))
        
        weight = portability[-3].find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score').text
        match = re.search(r'\(([\d.]+) kg\)', weight)
        if match:
            weight_in_kg = float(match.group(1))
            product.add_weight(weight_in_kg)
            
        # Get resolution
        resolution_card = self.get_card(driver, '5195')
        resolution = resolution_card.find_element(By.CLASS_NAME, 'test_value.is-word').find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score.ld-paywall').text
        product.add_screen_resolution(resolution)
        
        # Get processor
        processor_card = self.get_card(driver, '6096')
        brand = processor_card.find_element(By.CLASS_NAME, 'test_value.is-word').find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score.ld-paywall').text
        model = processor_card.find_element(By.CLASS_NAME, 'test_value.is-freeform').find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score.ld-paywall').text
        product.add_processor(brand + ' ' + model)
        
        return product
    
    def parse_mouse(self, product, driver):
        # Get wireless
        wireless_card = driver.find_element(locate_with(By.CLASS_NAME, 'test_group-header').below({By.ID: 'test_3018'}))
        wireless_score = float(wireless_card.find_element(By.CLASS_NAME, 'e-score_box-value').text)
        product.add_wireless(wireless_score > 0)
        
        # Get buttons
        buttons_card = self.get_card(driver, '3044')
        buttons = buttons_card.find_element(By.CLASS_NAME, 'test_value.is-number').find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score.ld-paywall').text
        product.add_buttons(int(buttons))
        
        # Get DPI
        dpi_card = self.get_card(driver, '12649')
        if dpi_card is not None:
            dpis = dpi_card.find_elements(By.CLASS_NAME, 'test_value.is-number')
            for dpi in dpis:
                max_label = dpi.find_element(By.CLASS_NAME, 'test_value-label').text
                if max_label == 'Maximum CPI':
                    max_dpi = dpi.find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score.ld-paywall').text
                    product.add_dpi(int(max_dpi.replace(' CPI', '').replace(',', '')))
                    break
        
        # Get weight
        weight_card = self.get_card(driver, '3002')
        weight = weight_card.find_elements(By.CLASS_NAME, 'test_value.is-number')[1].find_element(By.CLASS_NAME, 'test_result_value.e-test_result.review-value-score').text
        float_weight = float(weight.replace(' g', ''))
        product.add_weight(float_weight, False)

        return product
    
    # Helper methods
    def get_card(self, driver, test:str):
        test_str = 'test_' + test
        
        #Test if card exist 
        anchor = driver.find_elements(By.ID, test_str)
        if len(anchor) < 1:
            return None
        
        return driver.find_element(locate_with(By.CLASS_NAME, 'test_group-content').below({By.ID: test_str}))

        
        

def main():
    scrapper = rtings_scrapper()
    # scrapper.get_earbuds()
    # scrapper.get_headphones()
    # scrapper.get_keyboards()
    # scrapper.get_mice()
    scrapper.get_laptops()
    
    # scrapper.reset_names()
    # url = 'https://www.rtings.com/mouse/reviews/razer/viper-v3-pro'
    # driver = scrapper.start(url)
    # # scrapper.parse_recommendations('headphones', 'https://www.rtings.com/headphones/reviews/best/headphones')
    # Product = scrapper.categories['mouse']
    # product = Product(name='Razer Viper V3 Pro')
    # scrapper.parse_mouse(product, driver)
    # print(product.__str__())
    
    
    # Models not implemented yet
    # scrapper.get_television()
    # scrapper.get_monitors()
    
if __name__ == "__main__":
    main()
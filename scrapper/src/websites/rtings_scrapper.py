from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Scrapper import Scrapper
from src.models.product import Product

class rtings_scrapper(Scrapper):
    def __init__(self):
        super().__init__()
        self.website = 'https://www.rtings.com/'
    
    def get_headphones(self):
        pass
    
    def get_earbuds(self):
        pass
    
    def get_laptops(self):
        pass
    
    def get_mice(self):
        pass
    
    def get_monitors(self):
        pass
    
    def parse_recommendations(self, url:str):
        # driver go recommendation page
        driver = self.start(url)
        recommendations = driver.find_elements(By.CLASS_NAME, 'recommendation_page-block')
        for recommendation in recommendations:
            # Find and instantiate new product
            p_name = recommendation.find_element(By.CLASS_NAME, 'recommendation_page-block-name')
            product = Product(p_name.text.split('\n')[0])
            print(p_name.text.split('\n')[0])
            
            # Get link of review
            p_url = p_name.find_element(By.TAG_NAME, 'a').get_attribute('href')
            product.add_review(p_url)
            print(product.reviews)
            
            # Get recommendation reasons
            summary_block = recommendation.find_element(By.CLASS_NAME, 'e-rich_content')
            summary = summary_block.find_elements(By.TAG_NAME, 'p')
            for paragraphs in summary:
                # print(paragraphs.text)
                product.add_description(paragraphs.text)
            
            self.parse_review(product, p_url)
        self.end(driver)
    
    def parse_review(self, product:Product, url:str):
        driver = self.start(url)
        
        # Get description of product
        texts = driver.find_element(By.CLASS_NAME, 'product_page-header').find_element(By.CLASS_NAME, 'e-rich_content').find_elements(By.TAG_NAME, 'p')
        for text in texts:
            product.add_description(text.text.strip())
        print(product.description)
        
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
        print(product.pros)
        print(product.cons)
        
        
        self.end(driver)

def main():
    q = 'https://www.rtings.com/headphones/reviews/best/by-usage/gaming'
    scrapper = rtings_scrapper()
    scrapper.parse_recommendations(q)
    
if __name__ == "__main__":
    main()
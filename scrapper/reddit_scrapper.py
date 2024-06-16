import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from multiprocessing.pool import ThreadPool
from rapidfuzz import fuzz
from random import sample
from Scrapper import Scrapper

class reddit_scrapper(Scrapper):
    # Scrapper to scrape reddit comments of products to get general product sentiment
    def __new__(cls):
        # Overriding default creation of new instance, no point for more than 1 instance
        if not hasattr(cls, 'instance'):
            cls.instance = super(reddit_scrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.website = 'https://www.reddit.com'
        self.website_name = 'reddit.com'
    
    def get_methods(self) -> list:
        # return list of methods to call to get data for various categories
        return [
            self.update_products,
        ]
    
    def update_products(self, products:list) -> list:
        pool = ThreadPool(4)
        results = pool.map(self.update_product, products)
        products = list(results)
        pool.close()
        
        for product in products:
            print(product.__str__())
        
        return products
    
    def update_product(self, product):
        urls = self.get_posts(product)
        print(urls)
        
        for url in urls:
            comments = self.parse_post(url)
            product.add_reddit_comments(comments)
            
            # Waiting to prevent reddit from blocking
            time.sleep(5)
            
        return product
        
    def get_posts(self, product) -> list[str]:
        search_url = self.website + '/search/?q=' + product.get_name().lower() + '&type=link&t=year'
        driver = self.start(search_url)
        
        # Wait. Don't be too fast like a bot.
        driver.implicitly_wait(5)
        
        # Get posts about product
        posts = driver.find_elements(By.CSS_SELECTOR, '[data-testid="post-title"]')
        urls = []
        for post in posts:
            url = post.get_attribute('href')
            urls.append(url)
        
        # Filter out advertisments, reddit got too much posts advertising stuff
        filter_method = self.filter(['deal', 'Deal'], False)
        urls = list(filter(filter_method, urls))
        
        # Limit posts, no point scrapping too many posts
        if len(urls) > 10:
            urls = urls[:10]
        
        self.end(driver)
        return urls
    
    def parse_post(self, url:str) -> list[str]:
        driver = self.start(url)
        driver.implicitly_wait(5)
        comment_list = []
        
        # Parse title and post words
        title = driver.find_element(By.TAG_NAME, 'h1')
        post_content = driver.find_element(locate_with(By.CLASS_NAME, 'text-neutral-content').below(title)).find_element(By.TAG_NAME, 'p')
        comment_list.append(title.text)
        comment_list.append(post_content.text)
        
        # Parse comments
        comments_wrapper = driver.find_element(By.ID, 'comment-tree')
        comments = comments_wrapper.find_elements(By.XPATH, 'shreddit-comment[@depth="0"]')
        
        if len(comments) < 20: 
            # Allow more comments
            comments = comments_wrapper.find_elements(By.TAG_NAME, 'shreddit-comment')
        
        for comment in comments:
            # Check if comment deleted
            is_deleted = comment.get_attribute('is-comment-deleted')
            if is_deleted == 'true': continue
            
            comment_string = comment.find_element(By.ID, '-post-rtjson-content').text.replace('\n', '. ')
            
            # Reddit comments below 5 words kinda not worth
            if len(comment_string.split()) < 6: continue
            
            comment_list.append(comment_string)
        
        self.end(driver)
        return comment_list
            
def main():
    scrapper = reddit_scrapper()
    Product = scrapper.categories['mouse']
    products = [
        Product(name='Razer Viper V2 pro'), 
        Product(name='Pulsar X2V2'), 
        Product(name='Fantech Aria XD7'),
    ]
    products = scrapper.update_products(products)
    print(str(products))
    
    # url = 'https://www.reddit.com/r/MouseReview/comments/1abgqm3/razer_viper_v2_pro/'
    # product = scrapper.parse_post(product, url)
    # print(product.__str__())
    # print(len(product.reddit_comments))
    
    # scrapper.reset_names()
    # products = scrapper.parse_recommendations('mouse', 'https://www.pcmag.com/picks/the-best-computer-mice')
    # for product in products:
    #     print(product.__str__())
    
if __name__ == "__main__":
    main()
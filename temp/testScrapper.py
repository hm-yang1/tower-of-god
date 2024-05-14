from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class testScrapper:
    def __init__(self, query):
        self.query = query
        
        #move browser options to another file later
        self.firefox_options = webdriver.FirefoxOptions()
        self.firefox_options.set_preference("browser.privatebrowsing.autostart", True)

    def rtings_scrapper(self):
        #headphones, mice, monitors, tv
        #search
        driver = webdriver.Firefox(self.firefox_options)
        driver.get("https://www.rtings.com/")
        searchBar = driver.find_element(By.CLASS_NAME, 'searchbar-input')
        searchBar.send_keys(self.query + Keys.ENTER)
        driver.implicitly_wait(2)
        
        #process search results
        results = driver.find_elements(By.CLASS_NAME, 'searchbar_results-name')
        urls = []
        products = []
        for result in results:
            print(result.text)
            urls.append(result.get_attribute('href'))
        
        #get products from recommendation pages
        for url in urls[:5]:
            print(url)
            driver.get(url)
            driver.implicitly_wait(2)
            recommendations = driver.find_elements(By.CLASS_NAME, 'recommendation_page-block')
            for recommendation in recommendations:
                product = recommendation.find_element(By.CLASS_NAME, 'recommendation_page-block-name')
                print(product.text.split('\n')[0])
                products.append(product.text.split('\n')[0])
        print(products)
        driver.quit()
    
    # def reddit_scrapper(self):
    #     driver = webdriver.Firefox()
    
    def reddit_scrapper(self):
        # performs a google search but limited to reddit
        # scrapes reddit comments
        # doesn't get for deleted comments
        # only gets comments on the first page
        
        #search
        driver = webdriver.Firefox()
        driver.get("https://www.google.com/search?q=" + self.query)
        
        #get urls
        results = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
        urls = []
        for result in results:
            urls.append(result.get_attribute('href'))
        
        comments = []
        for url in urls[:5]:
            driver.get(url)
            driver.implicitly_wait(2)
            
            commentElements = driver.find_elements(By.ID, '-post-rtjson-content')
            for commentElement in commentElements:
                print(commentElement.text)
                comments.append(commentElement.text)
        print(comments)
        driver.quit()
        
def main():
    q = "best mouse"
    scrapper = testScrapper(q)
    # scrapper.rtings_scrapper()
    scrapper.reddit_scrapper()
    return

if __name__ == "__main__":
    main()
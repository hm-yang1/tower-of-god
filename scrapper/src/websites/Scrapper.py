from selenium import webdriver

class Scrapper:
    # A parent class for all scrappers
    # set options for the webdriver and some helpful functions
    def __init__(self):
        self.firefox_options = webdriver.FirefoxOptions()
        self.firefox_options.add_argument("-headless")
        self.firefox_options.set_preference("browser.privatebrowsing.autostart", True)
    
    def start(self, url = None):
        driver = webdriver.Firefox(self.firefox_options)
        driver.set_window_size(1980, 1080)
        driver.get(url)
        driver.implicitly_wait(2)
        return driver

    
    def end(self, webdriver):
        webdriver.quit()

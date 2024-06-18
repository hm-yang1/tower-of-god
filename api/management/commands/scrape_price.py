from multiprocessing.pool import ThreadPool
from typing import Any
from .scrape import Command
from scrapper.Scrapper import Scrapper

class Command(Command):
    help = "Scrape price for all products. Use after all products scrapped"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        scrapper = Scrapper()
        product_categories = scrapper.categories.values()
        
        for Product in product_categories:
            print('scrapping: ' + str(Product))
            
            queryset = Product.objects.all()
            pool = ThreadPool(6)
            products = pool.map(self.scrape_price, queryset)
            for product in products:
                product.save() 
            pool.close()
        
        print('finished scraping prices')
        return
    
    def scrape_price(self, product):
        scrapper = Scrapper()
        scrapper.get_price(product)
        print(product)
        return product
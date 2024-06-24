from multiprocessing.pool import ThreadPool
from typing import Any
from .scrape import Command
from scrapper.Scrapper import Scrapper

class Command(Command):
    help = "Scrape price for all products. Use after all products scrapped"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        scrapper = Scrapper()
        product_categories = scrapper.categories.values()
        
        pool = ThreadPool(len(product_categories))
        curried_func = lambda x: self.scrape_price_helper(x, scrapper)
        pool.map(curried_func, product_categories)
        
        return
    
    def scrape_price_helper(self, Product, scrapper):
        print('scrapping: ' + str(Product))
        for product in Product.objects.all():
            # Get img url
            scrapper.get_price(product)
            print(product.get_name())
            product.save()
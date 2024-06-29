from multiprocessing.pool import ThreadPool
from typing import Any
from .scrape import Command
from scrapper.Scrapper import Scrapper
from scrapper.reddit_scrapper import reddit_scrapper

class Command(Command):
    help = "Scrape reddit comments"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        scrapper = reddit_scrapper()
        product_categories = scrapper.categories.values()
        
        # pool = ThreadPool(len(product_categories))
        # curried_func = lambda x: self.helper(x, scrapper)
        # pool.map(curried_func, product_categories)
        # pool.close()
        
        for Product in product_categories:
            self.helper(Product, scrapper)
        
        return
    
    def helper(self, Product, scrapper):
        products = Product.objects.all()
        results = scrapper.update_products(products)

        # for result in results:
        #     print(result)
        #     result.save()
        #     print('success')
        
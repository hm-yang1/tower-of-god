from typing import Any
from .scrape import Command
from scrapper.Scrapper import Scrapper
from scrapper.reddit_scrapper import reddit_scrapper

class Command(Command):
    help = "Scrape reddit comments"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        scrapper = Scrapper()
        reddit = reddit_scrapper()
        product_categories = scrapper.categories.values()
        
        for Product in product_categories:
            print('scrapping: ' + str(Product))
            for product in Product.objects.all():
                # Get reddit comments
                reddit.update_product(product)
                
                print(product)
                
                product.save()
        return
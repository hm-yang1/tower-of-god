from typing import Any
from .scrape import Command
from scrapper.Scrapper import Scrapper

class Command(Command):
    help = "Scrape img url for all products"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        scrapper = Scrapper()
        product_categories = scrapper.categories.values()
        
        for Product in product_categories:
            print('scrapping: ' + str(Product))
            for product in Product.objects.all():
                # Get img url
                scrapper.get_img_url(product)
                print(product)
                product.save()
        return
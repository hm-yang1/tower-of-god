from typing import Any
from multiprocessing.pool import ThreadPool
from django.core.management.base import BaseCommand
from ai.gemini import Gemini
from scrapper.Scrapper import Scrapper


class Command(BaseCommand):
    help = "Command to do summarise review of products"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        ai = Gemini()
        scrapper = Scrapper()
        product_categories = scrapper.categories.values()
        
        for category in product_categories:
            print(category)
            products = category.objects.all()
            pool = ThreadPool(14)
            pool.map(ai.summarise_reviews, products)
            pool.close()
        
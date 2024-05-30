from typing import Any
from django.core.management.base import BaseCommand
from scrapper.rtings_scrapper import rtings_scrapper
from . import scrape_website

class Command(BaseCommand):
    help = "Scrape rtings.com data and save data to psql DB"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        methods = rtings_scrapper().get_methods()

        for method in methods:
           self.scrape_and_save(method)
        return
    
    def scrape_and_save(self, func):
        products = func()
        
        for product in products:
            # Should include checks if the product already exist
            # Logic:
            # If not exist, just save, return
            # If same review url, just return, dont save
            # If different review url, add to description, pros, cons and review then save
            product.save()

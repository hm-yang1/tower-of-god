from typing import Any
from .scrape import Command
from scrapper.rtings_scrapper import rtings_scrapper

class Command(Command):
    help = "Scrape rtings.com data and save data to psql DB"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        methods = rtings_scrapper().get_methods()
        for method in methods:
           self.scrape_and_save(method[0], method[1])
        return
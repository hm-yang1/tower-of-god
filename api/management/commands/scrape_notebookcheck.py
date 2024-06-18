from typing import Any
from .scrape import Command
from scrapper.notebookcheck_scrapper import notebookcheck_scrapper as scrapper

class Command(Command):
    help = "Scrape notebookecheck.net data and save data to psql DB"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        methods = scrapper().get_methods()
        for method in methods:
           self.scrape_and_save(method[0], method[1])
        return
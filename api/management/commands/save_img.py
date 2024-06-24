from typing import Any
import requests
from io import BytesIO
from .scrape import Command
from scrapper.Scrapper import Scrapper
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class Command(Command):
    help = "Save img to azure blob for all products"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        scrapper = Scrapper()
        product_categories = scrapper.categories.values()
        
        for Product in product_categories:
            print('Saving: ' + str(Product))
            for product in Product.objects.all():
                # Pass if there is already an image
                if product.get_img(): continue
                
                # Get img url
                img_url = product.get_img_url()
                print(img_url)
                
                if img_url:
                    # Get image content from url
                    file_content = self.get_img_from_url(img_url)
                    
                    if file_content:
                        # Define file name with url
                        file_name = product.get_name().split('/')[-1].replace(" ", '_') +'.jpg'
                        
                        # Save image to azure blob and get back url
                        file_path = default_storage.save(f'products/{file_name}', file_content)
                        product.add_img(file_path)
                        product.save()
        return
    
    def get_img_from_url(self, url:str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            file_content = ContentFile(response.content)
            return file_content
        except requests.exceptions.RequestException as e:
            print(e)
            print(url)
            return None

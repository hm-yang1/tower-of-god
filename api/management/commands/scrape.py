from typing import Any
from django.core.management.base import BaseCommand
from rapidfuzz import process, fuzz, utils

class Command(BaseCommand):
    help = "Parent command for scrapper commands"
    
    # List of names of products
    # earbuds_names = models.Earbuds.objects.values_list('name')
    
    def scrape_and_save(self, func, Product):
        # List of existing product names
        existing_names = list(Product.objects.values_list('name', flat=True))
        print('existing products: ' + str(existing_names))
        products = func()
        
        for product in products:
            # Should include checks if the product already exist
            # Logic:
            # If not exist, just save, return
            # If same review url, just return, dont save
            # If different review url, add to description, pros, cons and review then save
            
            if existing_names:
                common_name = process.extractOne(
                    product.get_name(), 
                    existing_names, 
                    scorer=fuzz.token_ratio, 
                    processor = utils.default_process, 
                    score_cutoff= 85
                )
                print('common product name: ' + str(common_name))
                if common_name and common_name[1] > 85:
                    existing_product = Product.objects.get(name=common_name[0])
                    
                    # Skip if same review url exist
                    if [url for url in product.get_reviews() if url in existing_product.get_reviews()]: continue
                    
                    existing_product.combine(product)
                    existing_product.save()
                    continue
                
            product.save()

def main():
    names = [
        'APPLE MACBOOK Pro 14 M3', 
        'Apple MacBook Air 13 (2024)', 
        'Lenovo Yoga 7i 16 (2023)', 
        'ASUS Vivobook 16 M1605 (2023)',
        'Lenovo IdeaPad Slim 3i Chromebook 14 (2023)',
        'Microsoft Surface Pro 8 (2021)',
        'Dell Alienware m18 R2 (2024)'
    ]
    
    name = 'Apple MacBook Pro 14 m4'
    
    print(process.extractOne(name, names, scorer=fuzz.token_ratio, processor=utils.default_process))

if __name__ == "__main__":
    main()
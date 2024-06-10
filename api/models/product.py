from datetime import date
from django.db import models

class Product(models.Model):
    # Model fields
    
    # name of product has to be unique
    name = models.CharField(max_length=255, unique=True)
    brand = models.CharField(max_length=255)
    
    # Image reference to aws s3 bucket, needs testing
    img = models.ImageField(upload_to='products/', null=True)
    
    price = models.FloatField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    score = models.IntegerField(blank=True, null=True)
    pros = models.JSONField(default=list, blank=True)
    cons = models.JSONField(default=list, blank=True)
    reviews = models.JSONField(default=list, blank=True)
    
    # Need to add function to fill in googable information, probably in scrapper
    
    class Meta:
        # Set this class as abstract
        abstract = True
    
    def __str__(self) -> str:
        result = self.name
        result += '\n' + self.brand
        # result += '\n' + 'Price: ' + self.price
        result += '\n' + self.description
        result += '\n' + str(self.pros)
        result += '\n' + str(self.cons)
        result += '\n' + str(self.reviews)
        return result
    
    def add_brand(self, name: str):
        self.brand = name
    
    def add_review(self, url: str):
        self.reviews.append(url)
    
    def add_pros(self, pro:str):
        self.pros.append(pro)
        
    def add_cons(self, con:str):
        self.cons.append(con)
    
    def add_description(self, des:str):
        if des.isspace(): return
        if self.description == '':
            self.description += des
            return
        self.description = self.description + "\n" + des
    
    def add_price(self, price: float):
        if self.price is not None:
            return
        self.price = price
        
    # def remove_duplicates(self):
    #     self.pros = list(set(self.pros))
    #     self.cons = list(set(self.cons))
    #     self.reviews = list(set(self.reviews))
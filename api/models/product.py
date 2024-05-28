from datetime import date
from django.db import models

class Product(models.Model):
    # Model fields
    
    # name of product has to be unique
    name = models.CharField(max_length=255, unique=True)
    brand = models.CharField(max_length=255, blank=True)
    
    # Image reference to aws s3 bucket, needs testing
    img = models.ImageField(upload_to='products/')
    
    MSRP = models.FloatField(blank=True)
    release_date = models.DateField(blank=True)
    description = models.TextField(blank=True)
    score = models.IntegerField(blank=True)
    pros = models.JSONField(default=list, blank=True)
    cons = models.JSONField(default=list, blank=True)
    reviews = models.JSONField(default=list, blank=True)
    
    # Need to add function to fill in googable information, probably in scrapper
    
    class Meta:
        # Set this class as abstract
        abstract = True
        # pass
    
    def __str__(self) -> str:
        result = self.name
        result += '\n' + self.description
        result += '\n' + str(self.pros)
        result += '\n' + str(self.cons)
        return result
    
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
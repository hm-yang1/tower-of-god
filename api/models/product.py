from datetime import date
import datetime
from email.policy import default
from django.db import models

class Product(models.Model):
    # Model fields
    
    # name of product has to be unique
    name = models.CharField(max_length=255, unique=True)
    brand = models.CharField(max_length=255)
    
    # Image reference to azure blob storage
    img = models.ImageField(max_length=1000, upload_to='products/', null=True)
    img_url = models.URLField(max_length=500, null=True, blank=True)
    
    price = models.FloatField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    
    # Fields for sentiment analysis of reddit comments
    score = models.IntegerField(blank=True, null=True)
    justification = models.TextField(blank=True)
    
    pros = models.JSONField(default=list, blank=True)
    cons = models.JSONField(default=list, blank=True)
    reviews = models.JSONField(default=list, blank=True)
    reddit_comments = models.JSONField(default=list, blank=True)
        
    class Meta:
        # Set this class as abstract
        abstract = True
    
    def __str__(self) -> str:
        result = self.name
        result += '\n' + self.brand
        result += '\n' + 'Price: ' + str(self.price)
        result += '\n' + 'Date: ' + str(self.review_date)
        result += '\n' + 'Score: ' + str(self.score)
        result += '\n' + self.justification
        result += '\n' + str(self.img_url)
        result += '\n' + self.description
        result += '\n' + 'Summary: ' + self.summary
        result += '\n' + str(self.pros)
        result += '\n' + str(self.cons)
        result += '\n' + str(self.reddit_comments) + str(len(self.reddit_comments))
        result += '\n' + str(self.reviews)
        return result
    
    def combine(self, product):
        # Combine 2 product instances of the same product together
        self.add_price(product.price)
        self.add_img_url(product.img_url)
        self.add_description(product.description)
        self.pros.extend(product.pros)
        self.cons.extend(product.cons)
        self.reviews.extend(product.reviews)

        # Choose earlier review date
        if self.review_date and product.review_date and self.review_date > product.review_date:
            self.review_date = product.review_date
        
        return self
    
    # Filter fields
    @classmethod
    def get_filters(cls) -> dict:
        return {
            'brand': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'review_date': ['exact', 'gte', 'lte'],
        }
    
    # For filter fields with unique results
    @classmethod
    def get_specific_filters(cls) -> dict:
        return ['brand']
    
    # Get order fields for product
    @classmethod
    def get_orders(cls) -> list:
        return ['price', 'review_date', 'score']
        
    def add_brand(self, name: str):
        self.brand = name
    
    def add_review(self, url: str):
        self.reviews.append(url)
    
    def add_pros(self, pro:str):
        self.pros.append(pro)
        
    def add_cons(self, con:str):
        self.cons.append(con)
        
    def add_reddit_comments(self, comments:list):
        self.reddit_comments.extend(comments)
    
    def add_description(self, des:str):
        if des.isspace(): return
        if self.description == '':
            self.description += des
            return
        self.description = self.description + "\n" + des
        
    def add_summary(self, summary:str):
        if summary.isspace(): return
        if len(summary.split()) > 1000: return
        self.summary = summary
    
    def add_score(self, score:int):
        if score > 10 or score < 0: return
        self.score = score
        
    def add_justification(self, justification:str):
        if justification.isspace(): return
        if len(justification.split()) > 100: return
        self.justification = justification
        
    def add_price(self, price: float):
        if self.price: return
        self.price = price
        
    def add_date(self, year:int, month:int, day:int):
        date = datetime.date(year, month, day)
        self.review_date = date
    
    def add_img_url(self, url:str):
        if self.img_url: return
        self.img_url = url
    
    def add_img(self, file_path:str):
        self.img.name = file_path
            
    def get_name(self) -> str:
        return self.name
    
    def get_price(self):
        return self.price
    
    def get_img_url(self) -> str:
        return self.img_url
    
    def get_img(self):
        return self.img
    
    def get_description(self) -> str:
        return self.description
    
    def get_summary(self) -> str:
        return self.summary
    
    def get_justification(self) -> str:
        return self.justification
    
    def get_reviews(self) -> list:
        return self.reviews
    
    def get_reddit_comments(self):
        return self.reddit_comments
        
    def remove_duplicates(self):
        self.pros = list(set(self.pros))
        self.cons = list(set(self.cons))
        self.reviews = list(set(self.reviews))
        self.reddit_comments = list(set(self.reddit_comments))
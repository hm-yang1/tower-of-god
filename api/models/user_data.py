from django.db import models
from user import User
from category import Category

# Models to store user data. 
# Includes: SearchHistory, Favourites
class SearcHistory(models):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_histories')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        result = self.user.username + ' searched ' 
        result += self.product_category.name + ': ' + self.product_id
        result += ' at ' + str(self.datetime)
        return result
    
class Favorite(SearcHistory):
    pass
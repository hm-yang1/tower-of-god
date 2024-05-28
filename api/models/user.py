from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.EmailField(max_length=254, unique=True)
    date_created = models.DateField(auto_now_add=True)
    
    # Set to false to prompt user to verify email
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    
    def __str__(self) -> str:
        return self.username + str(self.date_created)

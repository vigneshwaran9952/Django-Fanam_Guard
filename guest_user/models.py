from django.db import models


    
class GuestEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email    
    
class UserSettings(models.Model):
    email = models.EmailField(unique=True)

    country = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email    
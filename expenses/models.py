from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Expense(models.Model):
    id = models.AutoField(primary_key= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Expense')
    category = models.CharField(max_length=50)
    cost = models.IntegerField()
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    

   
    def __str__(self):
        return f"{self.category} - {self.description} - {self.cost}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.user.username
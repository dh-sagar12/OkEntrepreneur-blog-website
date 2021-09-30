from typing import ClassVar
from django.db import models

# Create your models here.

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=13)
    message = models.TextField(max_length=1000, default="")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    
    def __str__(self):
        return self.name

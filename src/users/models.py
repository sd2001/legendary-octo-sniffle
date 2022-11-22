from django.db import models
from django.contrib.auth.models import AbstractUser
import bcrypt

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50) # We will use bcrypt to hash it
    password_salt = models.CharField(max_length=255, default=bcrypt.gensalt())
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
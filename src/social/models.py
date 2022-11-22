from django.db import models
from django.contrib.postgres.fields import JSONField


from users.models import User

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField()
    comments_count = models.IntegerField()
    comments = models.JSONField(null=True)
    
    
class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.IntegerField()
    user_who_liked = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    user_followed = models.IntegerField()
    user_who_followed = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
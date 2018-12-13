from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Auto-incrementing ID included implicitly 

class Tag(models.Model):
    tag = models.CharField(max_length=32)
    posts = models.ManyToManyField('posts.Post')
    posts.null = True

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    rating = models.IntegerField()
    score = models.IntegerField()
    tags = models.ManyToManyField('posts.Tag')    
    updated_at = models.DateTimeField(auto_now=True)

class Brewser(AbstractUser):
    picture = models.CharField(max_length=255) 
    channels = models.ManyToManyField('posts.Tag')    

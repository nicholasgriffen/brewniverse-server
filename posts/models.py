from django.db import models

# Create your models here.
# Auto-incrementing ID included implicitly 

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    picture = models.CharField(max_length=255)
    score = models.IntegerField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
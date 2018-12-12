from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post 

class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = ('id', 'title', 'content', 'picture', 'score', 'rating', 'author')

    author = serializers.ReadOnlyField(source='author.id')

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields = ('id', 'username', 'email', 'posts')
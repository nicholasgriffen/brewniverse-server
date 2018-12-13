from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post, Tag 

class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag 
        fields = ['tag']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')
    tags = TagSerializer(many=True, read_only=True)
    class Meta: 
        model = Post
        fields = ('id', 
                'author',
                'content', 
                'picture', 
                'rating', 
                'score',
                'tags', 
                'title')


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    class Meta: 
        model = User 
        fields = ('id', 
                'username', 
                'email', 
                'posts')

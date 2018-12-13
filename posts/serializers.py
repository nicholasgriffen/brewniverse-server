from rest_framework import serializers
from posts.models import Post, Tag, Brewser

class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag 
        fields = ['tag', 'posts']

class PostSerializer(serializers.ModelSerializer):
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

class ChannelSerializer(TagSerializer):
    posts = PostSerializer(many=True, read_only=True)

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    channels = ChannelSerializer(many=True, read_only=True)
    
    class Meta: 
        model = Brewser 
        fields = ('id', 
                'username', 
                'email',
                'picture', 
                'posts',
                'channels',
                'password')
              #keyword args  
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Brewser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            picture=validated_data['picture']
        )
        # hash pw and save a hash
        user.set_password(validated_data['password'])
        user.save()

        return user
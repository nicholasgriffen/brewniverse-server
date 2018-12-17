from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from posts.models import Post, Tag, Brewser

class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag 
        fields = ['tag', 'posts']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    authorId = serializers.ReadOnlyField(source='author.id')
    
    tags = TagSerializer(many=True, read_only=False)
    class Meta: 
        model = Post
        fields = ('id', 
                'author',
                'authorId',
                'title', 
                'content',
                'picture', 
                'rating', 
                'score',
                'tags')
    def update(self, instance, validated_data):
        if 'score' in validated_data:
            if validated_data['score'] != instance.score:
                instance.score = validated_data['score']
                return instance

        newTags = []
        if 'tags' in validated_data:  
            for dataTag in validated_data['tags']:
                try:
                    found = Tag.objects.get(tag=dataTag['tag'])
                except ObjectDoesNotExist: 
                    found = Tag.objects.create(tag=dataTag['tag'])
                found.posts.add(instance)
                newTags = newTags + [found]

        instance.tags.set(newTags)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

class ChannelSerializer(TagSerializer):
    posts = PostSerializer(many=True, read_only=False)

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=False, required=False)
    channels = ChannelSerializer(many=True, read_only=False, required=False)
    
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

    def update(self, instance, validated_data):
        tags = []
        
        #update channels
        if 'channels' in validated_data:
            for channel in validated_data['channels']:
                tagInstance = Tag.objects.get(tag=channel['tag'])
                tags = tags + [tagInstance]
                
        #update password 
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.email = validated_data.get('email', instance.email)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.username = validated_data.get('username', instance.username)
        instance.channels.set(tags)
        instance.save()
        return instance
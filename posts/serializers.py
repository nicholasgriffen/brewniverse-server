import urllib
import hashlib

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
                
    def create(self, validated_data):
        instance = Post.objects.create(
            author=self.context['request'].user,
            title=validated_data['title'],
            content=validated_data['content'],
            picture=validated_data['picture'],
            rating=validated_data['rating'],
            score=validated_data['score']
        )
        modelTags = []
        # Iterate over request tags 
        if 'tags' in validated_data:
            for dataTag in validated_data['tags']:
                # Look up tag
                # Create if does not exist
                try:
                    found = Tag.objects.get(tag=dataTag['tag'].lower())
                except ObjectDoesNotExist: 
                    found = Tag.objects.create(tag=dataTag['tag'].lower())
                # accumulate            
                # associate post with tag
                modelTags = modelTags + [found]
                found.posts.add(instance)
            # call .set since instance is already saved
        instance.tags.set(modelTags)
        
        instance.save()

        return instance

    def update(self, instance, validated_data):
        if 'score' in validated_data:
            if validated_data['score'] != instance.score:
                instance.score = validated_data['score']

                instance.tags.set(instance.tags)
                
                instance.title = instance.title
                instance.content = instance.content
                instance.picture = instance.picture
                instance.rating = instance.rating
        
                instance.save()
                
                return instance

        newTags = []
        if 'tags' in validated_data:  
            for dataTag in validated_data['tags']:
                try:
                    found = Tag.objects.get(tag=dataTag['tag'].lower())
                except ObjectDoesNotExist: 
                    found = Tag.objects.create(tag=dataTag['tag'].lower())
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
    
    gravatar_default = "retro"
    gravatar_size = 150

    class Meta: 
        model = Brewser 
        fields = ('id', 
                'username', 
                'email',
                'picture', 
                'posts',
                'channels',
                'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
            'picture': {'required': False}            
        }

    def gravatar_url(self, email):
        return "https://www.gravatar.com/avatar/%s?%s" % (
            hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest(), 
            urllib.parse.urlencode({
                'd': self.gravatar_default, 
                's': str(self.gravatar_size)
                })
            )

    def create(self, validated_data):
        gravatar = self.gravatar_url(email=validated_data['email'])
        user = Brewser.objects.create(
            username=validated_data['username'].strip(),
            email=validated_data['email'].strip(),
            picture=gravatar
        )
        # hash pw and save a hash
        user.set_password(validated_data['password'].strip())
        
        user.save()

        return user

    def update(self, instance, validated_data):
        tags = []
        
        #update channels
        if 'channels' in validated_data:
            for channel in validated_data['channels']:
                try: 
                    tagInstance = Tag.objects.get(tag=channel['tag'].lower())
                except ObjectDoesNotExist:
                    tagInstance = Tag.objects.create(tag=channel['tag'].lower())
                tags = tags + [tagInstance]
                
        #update password 
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.channels.set(tags)

        instance.email = validated_data.get('email', instance.email)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.username = validated_data.get('username', instance.username)
       
        instance.save()

        return instance
from rest_framework import serializers
from posts.models import Post, Tag, Brewser

class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag 
        fields = ['tag', 'posts']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    authorId = serializers.ReadOnlyField(source='author.id')
    
    tags = TagSerializer(many=True, read_only=True)
    class Meta: 
        model = Post
        fields = ('id', 
                'author',
                'content',
                'authorId', 
                'picture', 
                'rating', 
                'score',
                'tags',
                'title')

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
        if hasattr(validated_data, 'channels'):
            for channel in validated_data['channels']:
                tagInstance = Tag.objects.get(tag=channel['tag'])
                tags = tags + [tagInstance]
            validated_data.pop('channels', None)
        
        instance.channels.set(tags)
        
        #update password 
        if hasattr(validated_data, 'password'):
            instance.set_password(validated_data['password'])
            validated_data.pop('password', None)

        #update anything else
        for key in validated_data:
            instance[key] = validated_data[key]

        return instance
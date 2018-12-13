from rest_framework import generics, permissions 
from django.core.exceptions import ObjectDoesNotExist

from posts.permissions import IsOwnerOrReadOnly

from posts.models import Tag
from posts.serializers import ChannelSerializer

from posts.models import Post
from posts.serializers import PostWithAuthorSerializer

from posts.models import Brewser
from posts.serializers import UserSerializer

# Read (all), Create
class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostWithAuthorSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        modelTags = []
        # Iterate over request tags 
        for dataTag in self.request.data['tags']:
            # Look up tag
            # Create if does not exist
            try:
                found = Tag.objects.get(tag=dataTag)
            except ObjectDoesNotExist: 
                found = Tag.objects.create(tag=dataTag)
            # accumulate            
            modelTags = modelTags + [found]
        # Hack, hardcoding author to the 1 existing user
        
        serializer.save(author=Brewser.objects.get(id=1))
        serializer.save(tags=modelTags)
# Read (one), Update, Delete
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostWithAuthorSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        #   IsOwnerOrReadOnly)
    # Brewser.objects.get(id=author.id)
# Read (all), Create
class UserList(generics.ListCreateAPIView):
    queryset = Brewser.objects.all()
    serializer_class = UserSerializer

# Read (one)
class UserDetail(generics.RetrieveAPIView):
    queryset = Brewser.objects.all()
    serializer_class = UserSerializer

class ChannelList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = ChannelSerializer

class ChannelDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = 'tag' 
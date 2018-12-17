from rest_framework import generics, permissions 
from django.core.exceptions import ObjectDoesNotExist

from posts.permissions import IsOwnerOrReadOnly

from posts.models import Tag
from posts.serializers import ChannelSerializer

from posts.models import Post
from posts.serializers import PostSerializer

from posts.models import Brewser
from posts.serializers import UserSerializer

# Read (all), Create
class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        # get an instance to be used to build tag association
        instance = serializer.save(author=self.request.user)
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
            # associate post with tag
            modelTags = modelTags + [found]
            found.posts.add(instance)
        # call .set since instance is already saved
        instance.tags.set(modelTags)
# Read (one), Update, Delete
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
# Read (all), Create
class UserList(generics.ListCreateAPIView):
    queryset = Brewser.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

# Read (one)
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brewser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

class ChannelList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = ()

class ChannelDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = 'tag' 
    permission_classes = ()
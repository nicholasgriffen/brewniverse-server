from rest_framework import generics, permissions 
from django.core.exceptions import ObjectDoesNotExist

from posts.permissions import IsAuthorOrReadOnly

from posts.models import Tag
from posts.serializers import ChannelSerializer

from posts.models import Post
from posts.serializers import PostSerializer

from posts.models import Brewser
from posts.serializers import UserSerializer

class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
class UserList(generics.ListCreateAPIView):
    queryset = Brewser.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brewser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)

class ChannelList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = ()

class ChannelDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = 'tag' 
    permission_classes = ()

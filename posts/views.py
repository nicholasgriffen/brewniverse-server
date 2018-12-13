from rest_framework import generics, permissions 
from django.core.exceptions import ObjectDoesNotExist

from posts.permissions import IsOwnerOrReadOnly

from posts.models import Tag
from posts.serializers import TagSerializer

from posts.models import Post
from posts.serializers import PostSerializer

from django.contrib.auth.models import User 
from posts.serializers import UserSerializer

# Read (all), Create
class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        #   IsOwnerOrReadOnly)

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

        serializer.save(tags=modelTags)
        # Hack, hardcoding author to the 1 existing user
        serializer.save(author=User.objects.get(id=1))
    
# Read (one), Update, Delete
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        #   IsOwnerOrReadOnly)

# Read (all)
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Read (one)
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
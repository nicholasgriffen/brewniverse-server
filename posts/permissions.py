from rest_framework import permissions
from posts.models import Post


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to restrict write access to object authors, 
    or user objects writing to themselves.
    """

    def has_object_permission(self, request, view, obj):
        # Permission open on GET, HEAD, OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if isinstance(obj, Post):
            # Write permission allowed to any user for a vote.
            if request.query_params.get('vote'):
                # Write permission restricted on unsafe non-vote operations.
                return (set(request.data.keys()) == set(['score']))
            else:
                # Write permission only allowed to post author.
                return obj.author == request.user
        else:
            # Write permission only allowed to self user.
            return obj == request.user

from django.urls import path, include 
from . import views

urlpatterns = [
    path('posts/', views.PostListCreate.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('channels/', views.TagList.as_view()),
    path('channels/<str:tag>', views.TagDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]
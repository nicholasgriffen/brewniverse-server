from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post, Brewser, Tag

class PostTests(APITestCase):
    def setUp(self):
        user = Brewser.objects.create(
            username='Digijan',
            email='digijan@test.net',
            picture='http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            password='janpass2018'
        )
        
        post = Post.objects.create(
            author=user,
            title='Duff Good',
            content='Duff Man right',
            picture='http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            rating=5,
            score=2,
        )
        
        duff = Tag.objects.create(tag='duff')
        duff.posts.add(post)
        beer = Tag.objects.create(tag='beer') 
        beer.posts.add(post)
        
        post.tags.set([duff, beer])
        
    def test_post_post(self):
        """
        POST to /posts/ with authenticated user creates new post with
        that user as author.
        """
        self.client.force_authenticate(user=Brewser.objects.get(username='Digijan'))
        url = '/posts/'
        
        data = {
            'title': 'Duff Not Good',
            'content': 'Duff Man wrong!',
            'picture': 'http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            'rating': 1,
            'score': 20,
            'tags': [{'tag':'duff'}, {'tag': 'beer'}, {'tag': 'terrible'}]
        }
        
        response = self.client.post(url, data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'id': 2,
            'author': 'Digijan',
            'authorId': 1,
            'title': 'Duff Not Good',
            'content': 'Duff Man wrong!',
            'picture': 'http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            'rating': 1,
            'score': 20,
            'tags': [{'tag':'duff', 'posts': [1, 2]}, {'tag': 'beer', 'posts': [1, 2]}, {'tag': 'terrible', 'posts':[2]}]
        })
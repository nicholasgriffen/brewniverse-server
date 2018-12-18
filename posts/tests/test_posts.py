from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post, Brewser, Tag

class PostTests(APITestCase):
    def setUp(self):
        digijan = Brewser.objects.create(
            username='Digijan',
            email='digijan@test.net',
            picture='http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            password='janpass2018'
        )

        notDigijan = Brewser.objects.create(
            username='NotDigijan',
            email='notdigijan@test.net',
            picture='http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            password='janpass2018'
        )

        post = Post.objects.create(
            author=digijan,
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
        
    def test_get_post(self):    
        """
        GET to /posts/:id retrieves Post matching :id
        """ 
        url = '/posts/1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': 1,
            'author': 'Digijan',
            'authorId': 1,
            'title': 'Duff Good',
            'content': 'Duff Man right',
            'picture': 'http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            'rating': 5,
            'score': 2,
            'tags': [{'tag':'duff', 'posts': [1]}, {'tag': 'beer', 'posts': [1]}]
        })

    def test_get_posts(self):    
        """
        GET to /posts/ retrieves Posts
        """ 
        url = '/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': 1,
            'author': 'Digijan',
            'authorId': 1,
            'title': 'Duff Good',
            'content': 'Duff Man right',
            'picture': 'http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            'rating': 5,
            'score': 2,
            'tags': [{'tag':'duff', 'posts': [1]}, {'tag': 'beer', 'posts': [1]}]
        }])

    def test_post_post(self):
        """
        POST to /posts/ with authenticated user creates new post with
        that user as author.
        """
        self.client.force_authenticate(user=Brewser.objects.get(id=1))
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
    def test_update_own_post(self):
        """
        PATCH to /posts/:id with authenticated user matching post author updates post
        """
        self.client.force_authenticate(user=Brewser.objects.get(id=1))
        url = '/posts/1'
        
        data = {'tags': [{'tag':'duffman'}]}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': 1,
            'author': 'Digijan',
            'authorId': 1,
            'title': 'Duff Good',
            'content': 'Duff Man right',
            'picture': 'http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            'rating': 5,
            'score': 2,
            'tags': [{'tag': 'duffman', 'posts': [1]}]
        })
    def test_update_other_post(self):
        """
        PATCH to /posts/:id?vote=true with authenticated user not matching post author
        does not update post if body contains attributes other than score
        """
        self.client.force_authenticate(user=Brewser.objects.get(id=2))
        url = '/posts/1?vote=true'
        
        data = {'title': 'Duff man is lame!'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.get(id=1).title, 'Duff Good')
    
    def test_upvote_other_post(self):
        """
        PATCH to /posts/:id?vote=true with authenticated user not matching post author
        does update post if body contains only score
        """
        self.client.force_authenticate(user=Brewser.objects.get(id=2))
        url = '/posts/1?vote=true'
        
        data = {'score': 10}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=1).score, 10)
        self.assertEqual(response.data, {
            'id': 1,
            'author': 'Digijan',
            'authorId': 1,
            'title': 'Duff Good',
            'content': 'Duff Man right',
            'picture': 'http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            'rating': 5,
            'score': 10,
            'tags': [{'tag':'duff', 'posts': [1]}, {'tag': 'beer', 'posts': [1]}]
        })
    def test_delete_other_post(self):
            """
            DELETE to /posts/:id with authenticated user not matching post author
            does not delete post
            """

            self.client.force_authenticate(user=Brewser.objects.get(id=2))
            url = '/posts/1'
            
            
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)            
            self.assertEqual(Post.objects.count(), 1)

    def test_delete_own_post(self):
            """
            DELETE to /posts/:id with authenticated user matching post author deletes post
            """

            self.client.force_authenticate(user=Brewser.objects.get(id=1))
            url = '/posts/1'
            
            
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Post.objects.count(), 0)
            self.assertEqual(response.data, None)

        

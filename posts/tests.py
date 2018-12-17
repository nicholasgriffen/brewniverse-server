from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Brewser

class BrewserTests(APITestCase):
    def test_create_brewser(self):
        """
        POST to /users/ creates a new Brewser.
        """
        url = '/users/'
        data = {
            'username': 'Digijan',
            'email': 'digijan@test.net',
            'picture': 'http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            'password': 'janpass2018'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Brewser.objects.count(), 1)
        self.assertEqual(Brewser.objects.get().username, 'Digijan')
    
    def test_get_brewser(self):
        """
        GET to /users/:id retrieves Brewser matching :id
        """ 
        testUser = Brewser.objects.create(
            username='Digijan',
            email='digijan@test.net',
            picture='http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            password='janpass2018'
        )
        url = '/users/1'
        response = self.client.get(url)
        self.assertEqual(response.data, {
            'id': 1,
            'username': 'Digijan',
            'email': 'digijan@test.net',
            'picture': 'http://cdn.forum280.org/logos/forum280_logo_no_tagline.png',
            'posts': [],
            'channels': []
        })
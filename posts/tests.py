from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Brewser

class BrewserTests(APITestCase):
    def test_create_brewser(self):
        """
        Ensure we can create a new Brewser object.
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
import json
import os 
import requests

from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from posts.models import Brewser

@tag('e2e', 'slow')
class ClientTest(APITestCase):
    urls = {
        'base': 'http://parallel-brewniverses.surge.sh/#/',
        'signup': 'signup',
        'home': 'all',
        'newPost': 'addpost',
        'login': 'login',
        'server': 'https://test-brew.herokuapp.com/'
    }
    testUser =  {
        'username': os.environ.get('TEST_USER_NAME', 'Please configure TEST_USER_NAME'),
        'password': os.environ.get('TEST_USER_PASS', 'Please configure TEST_USER_PASS')
    }
    newUser =  {
        'email': "nicholas@pb.com",
        'name': "Nicholas",
        'password': "d3e\/elop?me1nt",
    }
    post = {
        'title': 'Aromatic Arabic', 
        'picture': 'https://1.bp.blogspot.com/-Nb7Zo6yQrCI/VuIMp8pYnHI/AAAAAAAAHXY/FcTJPjojsZcVhEvD_-hcViuk6QTW6ZCZw/s1600/Aromatic%2BArabic%2BPhilz.JPG', 
        'rating': 5, 
        'content': 'Rich, tasty, beautiful brew', 
        'tags': 'coffee, dark roast, philz'   
    }
    
    def getTokenFromCookie(self):
        return self.browser.get_cookie('access_token')['value']

    def setUp(self):
        # disable image loading
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    
        options = webdriver.firefox.options.Options()
        # comment line below to run visible browser
        options.set_headless()
        
        self.browser = webdriver.Firefox(options=options, firefox_profile=firefox_profile)

        self.addCleanup(self.browser.quit)

    def testPageTitle(self):
        self.browser.get(self.urls['base'])
        self.assertEqual('Parallel Brewniverses', self.browser.title)
    
    def testSignup(self):
        urls = self.urls
        user = self.newUser
        
        self.browser.get(urls['base'] + urls['signup'])
        
        #create user
        email = self.browser.find_element_by_name('email')
        email.send_keys(user['email'])

        name = self.browser.find_element_by_name('name')        
        name.send_keys(user['name'])

        password = self.browser.find_element_by_name('pass')
        password.send_keys(user['password'])
        
        confPass = self.browser.find_element_by_name('confPass')
        confPass.send_keys(user['password'])
        
        confPass.submit()
    
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(urls['base'] + urls['home'])
        )
        
        # delete user
        access_token = self.getTokenFromCookie()
        user_id = self.browser.get_cookie('user_id')['value']

        headers = { 'Authorization': 'Bearer ' + str(access_token) }
        response = requests.delete(urls['server'] + 'users/' + user_id, headers=headers)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testPost(self):
        urls = self.urls
        post = self.post
        user = self.testUser

        # log in
        self.browser.get(urls['base'] + urls['login'])
        
        inputs = self.browser.find_elements_by_tag_name('input')
        
        inputs[0].send_keys(user['username'])
        inputs[1].send_keys(user['password'])

        inputs[1].submit()

        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(urls['base'] + urls['home'])
        )
        
        self.browser.find_element_by_xpath("//a[@href='#/addpost']").click()

        #submit post 
        title = self.browser.find_element_by_name('title')
        title.send_keys(post['title'])
        
        picture = self.browser.find_element_by_name('picture')
        picture.send_keys(post['picture'])

        rating = self.browser.find_element_by_name('rating')
        rating.send_keys(post['rating'])

        content = self.browser.find_element_by_name('content')
        content.send_keys(post['content'])

        tags = self.browser.find_element_by_name('channels')
        tags.send_keys(post['tags'])

        tags.submit()

        WebDriverWait(self.browser, 10).until(
            EC.url_contains('/post/')
        )

        # delete post 
        postId = self.browser.current_url.split('/').pop()
        access_token = self.getTokenFromCookie()

        headers = { 'Authorization': 'Bearer ' + str(access_token) }
        response = requests.delete(urls['server'] + 'posts/' + postId, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

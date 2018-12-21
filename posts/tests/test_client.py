import requests
from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from posts.models import Brewser

@tag('e2e', 'slow')
class ClientTest(APITestCase):

    data = {
        'urls': {
            'base': 'http://parallel-brewniverses.surge.sh/#/',
            'signup': 'signup',
            'home': 'all',
        },     
        
        'user': {
            'email': "nichos@pb.com",
            'name': "Nichas",
            'password': "development",
        }
    }

    def setUp(self):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        options = webdriver.firefox.options.Options()


        # options.set_headless()
        self.browser = webdriver.Firefox(options=options, firefox_profile=firefox_profile)
        self.addCleanup(self.browser.quit)

    def testPageTitle(self):
        self.browser.get(self.data['urls']['base'])
        self.assertEqual('Parallel Brewniverses', self.browser.title)
    
    def testSignupForm(self):
        # sign up
        urls = self.data['urls']
        user = self.data['user']
        
        self.browser.get(urls['base'] + urls['signup'])
        
        email = self.browser.find_element_by_name('email')
        email.send_keys(user['email'])

        name = self.browser.find_element_by_name('name')
        name.send_keys(user['name'])

        password = self.browser.find_element_by_name('pass')
        password.send_keys(user['password'])
        
        confPass = self.browser.find_element_by_name('confPass')
        confPass.send_keys(user['password'])
        
        confPass.submit()
        
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.url_to_be(urls['base'] + urls['home'])
            )
            # get authorization cookie 
            access_token = self.browser.get_cookie('access_token')['value']
            user_id = self.browser.get_cookie('user_id')['value']
            # log out 

            # delete user
            headers = { 'Authorization': 'Bearer ' + str(access_token) }
            
            response = requests.delete('https://test-brew.herokuapp.com/users/' + user_id, headers=headers)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        finally:
            self.browser.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rest_framework.test import APITestCase


class ClientTest(APITestCase):

    data = {
        'urls': {
            'base': 'http://parallel-brewniverses.surge.sh/#/',
            'signup': 'signup',
            'home': 'all',
        },
        
        'user': {
            'email': "dijan@test.net",
            'name': "dija",
            'password': "development",
        }
    }

    def setUp(self):
        options = webdriver.firefox.options.Options()
        # options.set_headless()
        self.browser = webdriver.Firefox(options=options)
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

        finally:
            self.browser.quit()
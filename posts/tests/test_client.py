from selenium import webdriver
from rest_framework.test import APITestCase


class ClientTest(APITestCase):
    baseClientUrl = 'http://parallel-brewniverses.surge.sh'
    
    def setUp(self):
        options = webdriver.firefox.options.Options()
        options.set_headless()
        self.browser = webdriver.Firefox(options=options)
        self.addCleanup(self.browser.quit)

    def testPageTitle(self):
        self.browser.get(self.baseClientUrl)
        self.assertIn('Parallel', self.browser.title)
from selenium import webdriver
from rest_framework.test import APITestCase


class ClientTest(APITestCase):
    baseClientUrl = 'http://parallel-brewniverses.surge.sh'
    signupUrl = '/#/signup'
    data = [
        user: {
            email: "digijan@test.net",
            name: "digijan",
            password: "development",
            confPass: "development"
        }
    ]

    def setUp(self):
        options = webdriver.firefox.options.Options()
        options.set_headless()
        self.browser = webdriver.Firefox(options=options)
        self.addCleanup(self.browser.quit)

    def testPageTitle(self):
        self.browser.get(self.baseClientUrl)
        self.assertEqual('Parallel Brewniverses', self.browser.title)
    
    def testSignupForm(self):
        self.brow
        form = self.browser.find_element_by_tag_name('form')
        form.submit()ser.get(self.baseClientUrl + self.signupUrl)
        user = self.data['user']

        email = self.browser.find_element_by_name('email')
        email.send_keys(user.email)

        name = self.browser.find_element_by_name('name')
        name.send_keys(user.name)
        
        password = self.browser.find_element_by_name('pass')
        password.send_keys(user.password)
        
        confPass = self.browser.find_element_by_name('confPass')
        confPass.send_keys(user.confPass)

        form = self.browser.find_element_by_tag_name('form')
        form.submit()

from django.test import Client, TestCase
from django.urls import reverse


class TestAccountView(TestCase):

    def test_login_view(self):
        client = Client()
        response = client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_logout_view(self):
        client = Client()
        response = client.get(reverse('logout'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

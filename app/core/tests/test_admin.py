from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        # The test client is a python class that acts as a dummy web browser
        # allowing you to test your views and interact with your Django-powered
        # application programmatically 
        # The reason we're doing a unit test on admin is because we're going to
        # customise the admin function later on and we need to test the views
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test123',
            name='test user full name'
        )

    def test_users_listed(self):
        """ Test that users are listed on user page """
        # admin is the app and core_user_changelist is the name of the url 
        url = reverse('admin:core_user_changelist')
        # perform a http get 
        res = self.client.get(url)

        # apart from keyword search, it also expects an http 200 response
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user page works """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that the create user page works """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
from django.test import TestCase
from .models import Shorten,Tracker
from django.contrib.auth import get_user_model
from django.urls import reverse
class RedirectResponseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="test123",
        )

    def test_tracker_exists(self):
        #redundent
        token = self.client.post(reverse("djangorestauth:rest_login"),{
            "username":"test",
            "password":"test123",
        }).json().get("key")
        #redundent
        shorten = self.client.post(reverse("shortner:create_short"),data = {
            "original":"https://example.com"
        },headers={
            "Authorization":"Token %s"%token
        })
        response = self.client.get(reverse("shortner:get_short",args=(Shorten.objects.first().short_id,)))
        self.assertTrue(Tracker.objects.exists())
        self.assertEqual(response.status_code,200)
    def test_token_generate(self):
        response = self.client.post(reverse("djangorestauth:rest_login"),{
            "username":"test",
            "password":"test123",
        })    
        self.assertEqual(response.status_code,200)
    def test_shorten_delete(self):
        #redundent
        token = self.client.post(reverse("djangorestauth:rest_login"),{
            "username":"test",
            "password":"test123",
        }).json().get("key")
        #redundent
        shorten = self.client.post(reverse("shortner:create_short"),data = {
            "original":"https://example.com"
        },headers={
            "Authorization":"Token %s"%token
        })
        response = self.client.delete(reverse("shortner:get_short",args=(Shorten.objects.first().short_id,)),
        headers = {
            "Authorization":"Token %s"%token
        })
        self.assertEqual(Shorten.objects.exists(),False)
    
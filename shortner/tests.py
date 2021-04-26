from django.test import TestCase
from .models import Shorten,Tracker
import random,string
from django.contrib.auth import get_user_model
from django.urls import reverse
class RedirectResponseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        chars = string.ascii_letters+string.digits
        user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="test123",
        )
        short_id = Shorten.objects.create(
            created_by=user,
            short_id="".join(random.choices(chars,k=12)),
            original="example.com"
        )
    def test_tracker_exists(self):
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
        token = self.client.post(reverse("djangorestauth:rest_login"),{
            "username":"test",
            "password":"test123",
        }).json().get("key")
        response = self.client.delete(reverse("shortner:get_short",args=(Shorten.objects.first().short_id,)),
        headers = {
            "Authorization":"Token %s"%token
        })
        self.assertEqual(Shorten.objects.exists(),False)
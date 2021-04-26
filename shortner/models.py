from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
class Shorten(models.Model):
    original = models.URLField(max_length=2083)
    short_id = models.CharField(max_length=12,unique=True,primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(get_user_model(),on_delete=models.SET_NULL,related_name="shorten",null=True)
    def __str__(self):
        return self.original
    class Meta:
        ordering = ("-created_on",)
class Tracker(models.Model):
    short_id = models.ForeignKey(Shorten,on_delete=models.CASCADE,related_name="tracker")
    ip = models.GenericIPAddressField()
    browser = models.CharField(max_length=200)
    device = models.CharField(max_length=30)
    logged_on = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ("-logged_on",)
    def __str__(self):
        return self.short_id.short_id
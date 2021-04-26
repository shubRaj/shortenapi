from django.contrib import admin
from .models import Shorten,Tracker
class AdminShorten(admin.ModelAdmin):
    search_fields = ("short_id","original","created_by__username")
    list_display = ("short_id","original","created_by")
class AdminTracker(admin.ModelAdmin):
    list_display = ("short_id","logged_on","device",)
    search_fields = ("short_id__short_id",)

admin.site.register(Shorten,AdminShorten)
admin.site.register(Tracker,AdminTracker)

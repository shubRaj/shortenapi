from rest_framework import serializers
from .models import Shorten,Tracker
class ShortenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shorten
        fields = (
            "original",
        )
class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        exclude = ("short_id","id")
class CreateShortenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shorten
        exclude = (
            "short_id",
            "created_on",
            "created_by",
        )
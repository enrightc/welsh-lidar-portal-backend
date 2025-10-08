from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    """
    Serializer for News model — defines which fields are returned in the API.
    """
    class Meta:
        model = News
        fields = ("id", "title", "content", "published_at")
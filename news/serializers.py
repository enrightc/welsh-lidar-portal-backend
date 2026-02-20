from rest_framework import serializers
from .models import News, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class NewsSerializer(serializers.ModelSerializer):
    """Serializer for News model — defines which fields are returned in the API."""

    # Return full tag objects so the frontend can render chips
    tags = TagSerializer(many=True, read_only=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = News
        fields = ("id", "title", "content", "published_at", "tags", "image")
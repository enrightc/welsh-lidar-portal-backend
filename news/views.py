from django.shortcuts import render
from rest_framework import generics
from .models import News
from .serializers import NewsSerializer

class NewsListView(generics.ListAPIView):
    """
    Return all published news items, newest first.
    """
    queryset = News.objects.filter(is_published=True).order_by("-published_at", "-id")
    serializer_class = NewsSerializer


class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

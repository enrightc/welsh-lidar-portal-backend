from django.db import models
from django.utils import timezone

"""
A model for displaying News and updates on the frontend.
"""


class Tag(models.Model):
    # Keep tag names short and unique so they work well in filters later
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    # Multiple tags per article (optional)
    tags = models.ManyToManyField(Tag, blank=True, related_name="news_items")

    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "News item"
        verbose_name_plural = "News"
        ordering = ["-published_at", "-id"]

    def __str__(self):
        return self.title
    
    def publish(self):
        """Helper to mark as published with timestamp"""
        self.is_published = True
        self.published_at = timezone.now()
        self.save()

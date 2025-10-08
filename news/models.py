from django.db import models
from django.utils import timezone

"""
A model for displaying News and updates on the frontend.
"""
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

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

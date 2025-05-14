from django.contrib.gis.db import models
from django.utils import timezone
# Import Point so we can create locations
# using longitude and latitude coordinates
from django.contrib.gis.geos import Point


class Record(models.Model):
    SITE_TYPE_CHOICES = [
        ('bank', 'Bank'),
        ('ditch', 'Ditch'),
        ('enclosure', 'Enclosure'),
        ('field_system', 'Field System'),
        ('industrial', 'Industrial'),
        ('industrial', 'Industrial'),
        ('mound', 'Mound'),
        ('pit', 'Pit'),
        ('settlement', 'Settlement'),
        ('trackway', 'Trackway'),
        ('other', 'Other'),
        ('unknown', 'Unknown')
        # Add more types as needed
    ]

    PERIOD_CHOICES = [
        ('neolithic', 'Neolithic'),
        ('bronze_age', 'Bronze Age'),
        ('iron_age', 'Iron Age'),
        ('roman', 'Roman'),
        ('medieval', 'Medieval'),
        ('post_medieval', 'Post Medieval'),
        ('modern', 'Modern'),
        ('unknown', 'Unknown')
    ]

    title = models.CharField(max_length=150)
    PRN = models.IntegerField()
    description = models.TextField()
    site_type = models.CharField(
        max_length=100,
        choices=SITE_TYPE_CHOICES
    )
    period = models.CharField(
        max_length=100,
        choices=PERIOD_CHOICES)
    date_recorded = models.DateField(default=timezone.now)
    location = models.PointField(srid=4326, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.PRN})"

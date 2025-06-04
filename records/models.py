from django.contrib.gis.db import models
from django.utils import timezone
# Import Point so we can create locations
# using longitude and latitude coordinates
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
User = get_user_model()


class Record(models.Model):
    """
    This model represents a record of an archaeological site.
    """
    SITE_TYPE_CHOICES = [
        ('bank', 'Bank'),
        ('ditch', 'Ditch'),
        ('enclosure', 'Enclosure'),
        ('field_system', 'Field System'),
        ('industrial', 'Industrial'),
        ('mound', 'Mound'),
        ('pit', 'Pit'),
        ('settlement', 'Settlement'),
        ('trackway', 'Trackway'),
        ('other', 'Other'),
        ('unknown', 'Unknown')
        # Add more types as needed
    ]

    MONUMENT_TYPE_CHOICES = [
        # Enclosure
        ('banjo_enclosure', 'Banjo enclosure'),
        ('curvilinear_enclosure', 'Curvilinear enclosure'),
        ('defended_enclosure', 'Defended enclosure'),
        ('causewayed_enclosure', 'Causewayed enclosure'),
        ('rectilinear_enclosure', 'Rectilinear enclosure'),
        ('hillfort', 'Hillfort'),
        ('promontory_fort', 'Promontory fort'),

        # Mound
        ('round_barrow', 'Round barrow'),
        ('cairn', 'Cairn'),
        ('platform_mound', 'Platform mound'),
        ('burial_mound', 'Burial mound'),

        # Field System
        ('field_system', 'Field system'),
        ('ridge_and_furrow', 'Ridge and furrow'),
        ('lynchet', 'Lynchet'),
        ('strip_field_system', 'Strip field system'),

        # Settlement
        ('roman_villa', 'Roman villa'),
        ('farmstead', 'Farmstead'),
        ('hamlet', 'Hamlet'),
        ('deserted_medieval_village', 'Deserted medieval village'),

        # Trackway
        ('hollow_way', 'Hollow way'),
        ('trackway', 'Trackway'),
        ('causeway', 'Causeway'),

        # Industrial
        ('tramway', 'Tramway'),
        ('quarry', 'Quarry'),
        ('mine_shaft', 'Mine shaft'),
        ('leat', 'Leat'),
        ('mill', 'Mill'),

        # Pit
        ('quarry_pit', 'Quarry pit'),
        ('extraction_pit', 'Extraction pit'),

        # Bank
        ('boundary_bank', 'Boundary bank'),
        ('defensive_bank', 'Defensive bank'),
        ('field_boundary', 'Field boundary'),

        # Ditch
        ('defensive_ditch', 'Defensive ditch'),
        ('drainage_ditch', 'Drainage ditch'),
        ('boundary_ditch', 'Boundary ditch'),

        # Other
        ('earthwork', 'Earthwork'),
        ('cropmark', 'Cropmark'),
        ('structure', 'Structure (undefined)'),
        ('other', 'Other'),

        # Unknown
        ('unknown', 'Unknown'),
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

    recorded_by = models.ForeignKey(
        'users.User',  # Assuming you have a custom user model in users app
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=150)
    PRN = models.IntegerField()
    description = models.TextField()
    site_type = models.CharField(
        max_length=100,
        choices=SITE_TYPE_CHOICES
    )
    monument_type = models.CharField(
        max_length=100,
        choices=MONUMENT_TYPE_CHOICES,
        default=""
    )
    period = models.CharField(
        max_length=100,
        choices=PERIOD_CHOICES)
    date_recorded = models.DateField(default=timezone.now)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    picture1 = models.ImageField(
        blank=True, null=True, upload_to="pictures/%Y/%m/%d/")
    picture2 = models.ImageField(
        blank=True, null=True, upload_to="pictures/%Y/%m/%d/")
    picture3 = models.ImageField(
        blank=True, null=True, upload_to="pictures/%Y/%m/%d/")
    picture4 = models.ImageField(
        blank=True, null=True, upload_to="pictures/%Y/%m/%d/")
    picture5 = models.ImageField(
        blank=True, null=True, upload_to="pictures/%Y/%m/%d/")

    def __str__(self):
        return f"{self.title} ({self.PRN})"

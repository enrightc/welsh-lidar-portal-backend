from django import forms  # Django's form library for building forms
from .models import Record  # Import the Record model to tie the form to
from django.contrib.gis.geos import Point  # Import Point for geospatial data


# This form is used to create or update Record instances, including geospatial data.
class RecordsForm(forms.ModelForm):
    # The Meta class specifies model and fields to include in the form.
    class Meta:
        # Link the form to the Record model
        model = Record
        # List all the fields from Record to be exposed in the form, including lat/lon for coordinate entry
        fields = [
            'title', 'PRN', 'description', 'site_type', 'period', 'date_recorded',
            'location', 'latitude', 'longitude'
        ]
    # These fields are not part of the Record model, but are used to capture user input for latitude and longitude.
    latitude = forms.FloatField()   # User enters latitude as a float
    longitude = forms.FloatField()  # User enters longitude as a float

    def clean(self):
        data = super().clean()  # First, run Django's default validation and return the cleaned form data.
        latitude = data.pop('latitude')  # Get the latitude value from the form (and remove it from the data).
        longitude = data.pop('longitude')  # Get the longitude value from the form (and remove it from the data).
        data['location'] = Point(latitude, longitude, srid=4326)  # Create a geospatial Point using (lon, lat), and add it back to the form data.
        return data  # Return the updated data dictionary.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the default form setup.
        location = self.initial.get('location')  # Try to get the existing location value from the initial data.
        if isinstance(location, Point):  # Make sure the location is a proper Point object.
            self.initial['latitude'] = location.tuple[0]
            self.initial['longitude'] = location.tuple[1]

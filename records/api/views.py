from .serializers import RecordSerializer
from records.models import Record
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.db import transaction
from ..email_notifications import notify_her_of_record


class RecordList(generics.ListAPIView):
    """
    API view to retrieve a list of all records.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

class RecordCreate(generics.CreateAPIView):
    """
    When someone submits a the frontend form, the react app sends a POST request to the Django backend Post /api.records.create/
    This request hits the RecordCreate view, specfically the perform_create method. 
    API view that allows users to create a new record.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    # Take the form data.
    # use RecordSerializer to check it's valid.
    # Call perform_create() to save the record.
    def perform_create(self, serializer):
        if Record.objects.count() >= 500:
            raise ValidationError({"detail": "Opps, we are really sorry about this, but it looks like the database is currently full. We can not save your record right now. Please bear with us."})
        
        
         # Save the record first
         #serializer.save() creates a new record object in the database.
         # recorded_by=self.request.user adds the currently logged in user to the new record.
         # The result is returned to Django as the actual Python object it just created - the record variable.
        record = serializer.save(recorded_by=self.request.user)

        # immediately after the save Send the email
        # When database transaction finishes successfully, Django calls notify_her_of_record(record) which builds and sends the email with the record details to the HER. 
        transaction.on_commit(lambda: notify_her_of_record(record))

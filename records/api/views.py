from .serializers import RecordSerializer
from records.models import Record
from rest_framework import generics
from rest_framework.exceptions import ValidationError


class RecordList(generics.ListAPIView):
    """
    API view to retrieve a list of all records.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

class RecordCreate(generics.CreateAPIView):
    """
    API view that allows users to create a new record.
    When a POST request is sent to this view (with the right data), it will use the RecordSerializer to validate and save a new record to the database.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


    def perform_create(self, serializer):
        if Record.objects.count() >= 500:
            raise ValidationError({"detail": "Opps, we are really sorry about this, but it looks like the database is currently full. We can not save your record right now. Please bear with us."})
        serializer.save(recorded_by=self.request.user)

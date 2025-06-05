from .serializers import RecordSerializer
from records.models import Record
from rest_framework import generics


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

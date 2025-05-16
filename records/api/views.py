from .serializers import RecordSerializer
from records.models import Record
from rest_framework import generics


class RecordList(generics.ListAPIView):
    """
    API view to retrieve a list of all records.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

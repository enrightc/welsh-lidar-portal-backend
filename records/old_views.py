from rest_framework import viewsets
from .models import Record
from rest_framework.permissions import IsAuthenticated


# Class to handle API requests for the Record model, using Django REST Framework's ModelViewSet. This turns the Django model into a full
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()  #shows all records when someone visits the API
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]  # only logged in uesers can access the API


    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

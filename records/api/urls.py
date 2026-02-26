from django.urls import path
from .views import RecordList, RecordCreate, export_records_csv, export_records_geojson

urlpatterns = [
    path("records/", RecordList.as_view(), name="record-list"),
    path("records/create/", RecordCreate.as_view(), name="record-create"),
    path("records/export/csv/", export_records_csv, name="record-export-csv"),
    path("records/export/geojson/", export_records_geojson, name="record-export-geojson"),
]
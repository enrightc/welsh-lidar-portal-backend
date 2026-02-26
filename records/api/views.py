from .serializers import RecordSerializer
from records.models import Record
from rest_framework import generics
from rest_framework.exceptions import ValidationError
import csv
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_records_csv(request):
    """Download the current user's records as a CSV file."""

    # Only export the signed-in user's records
    qs = Record.objects.filter(recorded_by=request.user).order_by("-id")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="records.csv"'

    writer = csv.writer(response)

    # Export all concrete fields on the Record model (auto stays in sync)
    field_names = [f.name for f in Record._meta.fields]
    writer.writerow(field_names)

    for r in qs:
        row = []
        for name in field_names:
            field = Record._meta.get_field(name)

            # ForeignKeys: write the raw ID (e.g. recorded_by_id)
            if field.is_relation and field.many_to_one:
                value = getattr(r, f"{name}_id", "")
            else:
                value = getattr(r, name, "")

            # Geometry fields: convert to WKT so it stays usable
            if hasattr(value, "wkt"):
                value = value.wkt

            if value is None:
                value = ""

            row.append(value)

        writer.writerow(row)

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_records_geojson(request):
    """Download the current user's records as a GeoJSON FeatureCollection."""

    qs = Record.objects.filter(recorded_by=request.user).order_by("-id")

    def _to_ring(coords):
        """Convert stored coords (likely Leaflet lat/lng) to a GeoJSON ring (lng/lat) and close it."""
        if not coords:
            return None

        ring = []
        for pt in coords:
            lat = lng = None

            # Accept {lat: .., lng: ..}
            if isinstance(pt, dict):
                lat = pt.get("lat")
                lng = pt.get("lng")

            # Accept [lat, lng] or (lat, lng)
            elif isinstance(pt, (list, tuple)) and len(pt) >= 2:
                lat, lng = pt[0], pt[1]

            if lat is None or lng is None:
                continue

            # GeoJSON expects [lng, lat]
            ring.append([float(lng), float(lat)])

        if len(ring) < 3:
            return None

        # Close ring if needed
        if ring[0] != ring[-1]:
            ring.append(ring[0])

        return ring

    features = []

    for r in qs:
        # Try to interpret polygonCoordinate as a list of points.
        coords = getattr(r, "polygonCoordinate", None)

        # Some DB fields may store JSON as a string; try to parse if needed.
        if isinstance(coords, str):
            try:
                coords = json.loads(coords)
            except Exception:
                coords = None

        ring = _to_ring(coords) if coords else None

        geometry = None
        if ring:
            geometry = {
                "type": "Polygon",
                "coordinates": [ring],
            }

        props = {
            "id": r.id,
            "title": getattr(r, "title", ""),
            "description": getattr(r, "description", ""),
            "PRN": getattr(r, "PRN", ""),
            "site_type": getattr(r, "site_type", ""),
            "monument_type": getattr(r, "monument_type", ""),
            "period": getattr(r, "period", ""),
            "date_recorded": str(getattr(r, "date_recorded", "")) if getattr(r, "date_recorded", None) else "",
            "recorded_by": getattr(r, "recorded_by_id", ""),
        }

        # Include image URLs if present (use absolute URLs so QGIS can open them)
        for i in range(1, 6):
            field_name = f"picture{i}"
            f = getattr(r, field_name, None)
            if f and hasattr(f, "url"):
                props[field_name] = request.build_absolute_uri(f.url)
            else:
                props[field_name] = ""

        features.append({
            "type": "Feature",
            "geometry": geometry,
            "properties": props,
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    resp = HttpResponse(json.dumps(geojson), content_type="application/geo+json")
    resp["Content-Disposition"] = 'attachment; filename="records.geojson"'
    return resp

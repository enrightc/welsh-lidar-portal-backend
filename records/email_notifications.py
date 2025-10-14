from django.conf import settings
from django.core.mail import EmailMessage
import json

# Try to import GeoDjango helpers (safe if not installed)
try:
    from django.contrib.gis.geos import GEOSGeometry, Polygon, LinearRing
except Exception:
    GEOSGeometry = None
    Polygon = None
    LinearRing = None


def _geometry_from_jsonish(value):
    """
    Build a GEOSGeometry POLYGON (EPSG:4326) from common frontend shapes:
      - GeoJSON dict: {"type":"Polygon","coordinates":[ [ [lng,lat], ... ] ]}
      - Leaflet arrays: [ [lat,lng], ... ]  (we auto-swap to [lng,lat])
      - Arrays of dicts: [ {"lat":..,"lng":..}, ... ]
      - Nested single ring: [ [ [lat,lng], ... ] ]
    Returns None if we can't build a valid polygon.
    """
    if GEOSGeometry is None or Polygon is None or LinearRing is None or value is None:
        return None

    # Parse JSON string to python
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except Exception:
            return None

    # GeoJSON Polygon dict
    if isinstance(value, dict) and value.get("type") == "Polygon" and "coordinates" in value:
        try:
            geom = GEOSGeometry(json.dumps(value))
            if not geom.srid:
                geom.srid = 4326
            return geom
        except Exception:
            return None

    # Helper to normalize any input to a single ring of [lon,lat] pairs
    def normalize_to_ring(v):
        # List of dicts [{lat,lng}, ...]
        if isinstance(v, (list, tuple)) and v and isinstance(v[0], dict):
            out = []
            for d in v:
                if "lng" in d and "lat" in d:
                    out.append([float(d["lng"]), float(d["lat"])])
                elif "longitude" in d and "latitude" in d:
                    out.append([float(d["longitude"]), float(d["latitude"])])
                else:
                    return None
            return out

        # Nested single-ring [[[x,y],...]]
        if isinstance(v, (list, tuple)) and v and isinstance(v[0], (list, tuple)) and isinstance(v[0][0], (list, tuple)):
            return normalize_to_ring(v[0])

        # Flat list of coordinate pairs [[x,y],...]
        if isinstance(v, (list, tuple)) and v and isinstance(v[0], (list, tuple)) and len(v[0]) >= 2:
            try:
                first_x, first_y = float(v[0][0]), float(v[0][1])
            except Exception:
                return None

            # Detect [lat,lng] vs [lng,lat] using valid ranges
            is_latlng = (-90.0 <= first_x <= 90.0) and (-180.0 <= first_y <= 180.0)

            if is_latlng:
                pairs = [[float(p[1]), float(p[0])] for p in v]  # swap to [lon,lat]
            else:
                pairs = [[float(p[0]), float(p[1])] for p in v]  # already [lon,lat]
            return pairs

        return None

    ring = normalize_to_ring(value)
    if ring is None:
        return None

    # Ensure closed ring and minimum 4 points
    if ring[0] != ring[-1]:
        ring = ring + [ring[0]]
    if len(ring) < 4:
        return None

    try:
        lr = LinearRing(ring)
        poly = Polygon(lr)
        poly.srid = 4326
        return poly
    except Exception:
        return None


def _get_geometry(record):
    """
    Try to fetch a geometry from common field names or construct one
    from JSON/text fields like 'polygonCoordinate'.
    """
    # 1) Direct GeoDjango geometry fields
    for attr in ("geometry", "geom", "polygon", "shape"):
        if hasattr(record, attr):
            geom = getattr(record, attr)
            if geom is not None:
                return geom

    # 2) JSON/text-based polygon fields produced by the frontend
    for attr in ("polygonCoordinate", "polygon_coordinates", "coordinates", "polygon_json"):
        if hasattr(record, attr):
            raw = getattr(record, attr)
            if raw:
                built = _geometry_from_jsonish(raw)
                if built is not None:
                    return built

    return None


def notify_her_of_record(record):
    """
    Email the HER with record details, include the geometry as WKT in the body,
    and attach a GeoJSON file when geometry is present.

    Using fail_silently=True so submissions never crash due to SMTP.
    """
    to_list = getattr(settings, "HER_NOTIFY_TO", [])
    if not to_list:
        return  # skip if no address set

    record_url = f"{settings.SITE_BASE_URL}/record/{record.pk}"
    map_url = f"{settings.SITE_BASE_URL}/LidarPortal?recordId={record.pk}"

    subject = f"[New LiDAR Submission] {getattr(record, 'title', '')} (PRN: {getattr(record, 'PRN', None) or 'n/a'})"

    # Simple display values
    recorded_by_display = str(getattr(record, "recorded_by", "") or "n/a")
    date_recorded_display = str(getattr(record, "date_recorded", "") or "n/a")

    # Base body
    body = (
        "New community submission on the Welsh LiDAR Portal\n\n"
        f"Title: {getattr(record, 'title', '')}\n"
        f"PRN: {getattr(record, 'PRN', None) or 'n/a'}\n"
        f"Site type: {getattr(record, 'site_type', '')}\n"
        f"Monument type: {getattr(record, 'monument_type', '')}\n"
        f"Period: {getattr(record, 'period', '')}\n"
        f"Recorded by: {recorded_by_display}\n"
        f"Date recorded: {date_recorded_display}\n\n"
        f"Description:\n{getattr(record, 'description', '')}\n\n"
        f"View on map: {map_url}\n"
        f"Record page: {record_url}\n"
    )

    # --- Geometry handling: add WKT and build GeoJSON attachment ---
    geojson_bytes = None
    try:
        geom = _get_geometry(record)
        if geom and GEOSGeometry is not None:
            g = geom

            # Ensure WGS84 for portability
            try:
                if hasattr(g, "srid") and g.srid and g.srid != 4326 and hasattr(g, "transform"):
                    g.transform(4326)
            except Exception as e:
                print(f"[email_notifications] Transform to EPSG:4326 failed: {e}")

            # Add WKT inline
            if hasattr(g, "wkt"):
                body += "\nGeometry (WKT, EPSG:4326 if transform succeeded):\n"
                body += f"{g.wkt}\n"

            # Build GeoJSON FeatureCollection attachment
            try:
                geometry_geojson = json.loads(g.geojson) if hasattr(g, "geojson") else None
                if geometry_geojson:
                    feature = {
                        "type": "Feature",
                        "geometry": geometry_geojson,
                        "properties": {
                            "id": record.pk,
                            "title": getattr(record, "title", ""),
                            "PRN": getattr(record, "PRN", None),
                            "site_type": getattr(record, "site_type", ""),
                            "monument_type": getattr(record, "monument_type", ""),
                            "period": getattr(record, "period", ""),
                            "recorded_by": recorded_by_display,
                            "date_recorded": date_recorded_display,
                            "record_url": record_url,
                            "map_url": map_url,
                        },
                    }
                    fc = {"type": "FeatureCollection", "features": [feature]}
                    geojson_bytes = json.dumps(fc, ensure_ascii=False, indent=2).encode("utf-8")
            except Exception as e:
                print(f"[email_notifications] Failed to build GeoJSON: {e}")
        else:
            print("[email_notifications] No geometry found on record (checked geometry/geom/polygon/shape and polygonCoordinate-like fields).")
    except Exception as e:
        print(f"[email_notifications] Geometry extraction failed: {e}")

    # --- Send email (attach GeoJSON if available) ---
    try:
        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_list,
        )
        if geojson_bytes:
            filename = f"record-{record.pk}.geojson"
            msg.attach(filename, geojson_bytes, "application/geo+json")
        msg.send(fail_silently=True)  # never crash submissions on SMTP hiccups
    except Exception as e:
        print(f"[email_notifications] Failed to send HER email: {e}")
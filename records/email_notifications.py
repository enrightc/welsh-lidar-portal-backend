from django.conf import settings
from django.core.mail import send_mail

def notify_her_of_record(record):
    """
    Simple email: prints to terminal for now.
    Later we'll make it send real mail.
    """
    to_list = getattr(settings, "HER_NOTIFY_TO", [])
    if not to_list:
        return  # skip if no address set

    record_url = f"{settings.SITE_BASE_URL}/record/{record.pk}"
    map_url = f"{settings.SITE_BASE_URL}/LidarPortal?recordId={record.pk}"

    subject = f"[New LiDAR Submission] {record.title} (PRN: {record.PRN or 'n/a'})"

    body = (
        "New community submission on the Welsh LiDAR Portal\n\n"
        f"Title: {record.title}\n"
        f"PRN: {record.PRN or 'n/a'}\n"
        f"Site type: {record.site_type}\n"
        f"Monument type: {record.monument_type}\n"
        f"Period: {record.period}\n\n"
        f"Description:\n{record.description}\n\n"
        f"View on map: {map_url}\n"
        f"Record page: {record_url}\n"
    )

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=to_list,
        fail_silently=True,
    )
from django.contrib import admin
from records.models import Record
from .forms import RecordsForm
# Register your models here.


class RecordAdmin(admin.ModelAdmin):
    form = RecordsForm


admin.site.register(Record, RecordAdmin)

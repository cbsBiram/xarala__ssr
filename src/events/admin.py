from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Event, Speaker


class EventAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)


admin.site.register(Event, EventAdmin)
admin.site.register(Speaker)

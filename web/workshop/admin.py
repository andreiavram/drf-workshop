from django.contrib import admin

# Register your models here.
from workshop.models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ["name", "channel"]


admin.register(DeviceAdmin, Device)
from django.contrib import admin

# Register your models here.
from workshop.models import Device


class DeviceAdmin(admin.ModelAdmin):
    class Meta:
        model = Device


admin.register(DeviceAdmin, Device)
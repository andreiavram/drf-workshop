from django.contrib import admin

# Register your models here.
from workshop.models import Device, MessageHistory, RuleSet, Rule


class DeviceAdmin(admin.ModelAdmin):

    list_display = ['name', 'channel']


class MessageHistoryAdmin(admin.ModelAdmin):

    list_display = ['device', 'value']


class RuleSetAdmin(admin.ModelAdmin):

    list_display = ['target_device', 'payload']


class RuleAdmin(admin.ModelAdmin):

    list_display = ['ruleset', 'source_device', 'ref_value', 'operator']


admin.site.register(Device)
admin.site.register(MessageHistory, MessageHistoryAdmin)
admin.site.register(RuleSet, RuleSetAdmin)
admin.site.register(Rule, RuleAdmin)

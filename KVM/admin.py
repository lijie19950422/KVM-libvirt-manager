from django.contrib import admin
from KVM.models import KVMUser
from KVM.models import CMDB
# Register your models here.
class KVMUser_Style(admin.ModelAdmin):
    fieldsets = (
        ['must', {
            'fields': ('username',)
        }],
        ['select', {
            'classes': ('collapse',),
            'fields': ('passwd',)
        }]
    )
    list_display = ('username', 'id')
    search_fields = ('username',)
    list_filter = ('username',)
admin.site.register(KVMUser,KVMUser_Style)


class CMDB_Style(admin.ModelAdmin):
    fieldsets = (
        ['must', {
            'fields': ('hostname',)
        }],
        ['must', {
            'fields': ('IP',)
        }],
        ['must', {
            'fields': ('gateway',)
        }],
        ['must', {
            'fields': ('mac',)
        }],
        ['must', {
            'fields': ('distribution',)
        }],
        ['must', {
            'fields': ('distribution_version',)
        }],
        ['must', {
            'fields': ('architecture',)
        }],
        ['must', {
            'fields': ('kernel',)
        }],
        ['must', {
            'fields': ('processor',)
        }],
        ['must', {
            'fields': ('processor_cores',)
        }],
        ['must', {
            'fields': ('processor_count',)
        }]
    )
    list_display = ('hostname', 'IP')
    search_fields = ('hostname',)
    list_filter = ('hostname',)
admin.site.register(CMDB, CMDB_Style)

from django.contrib import admin
from .models import Regalia, Operation, File


class RegaliaAdmin(admin.ModelAdmin):
    ordering = ['full_name']
    list_display = ['full_name', 'rank', 'city']


admin.site.register(Regalia, RegaliaAdmin)
admin.site.register(Operation)
admin.site.register(File)

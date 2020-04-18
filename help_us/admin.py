from django.contrib import admin

from .models import *


class WRAdmin(admin.ModelAdmin):
    readonly_fields = ('date', )


admin.site.register(WorkRequest, WRAdmin)
admin.site.register(Resume)
# Register your models here.

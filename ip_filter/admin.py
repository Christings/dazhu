from django.contrib import admin
import models
# Register your models here.
class IPAdmin(admin.ModelAdmin):
    list_display = ('body', )

admin.site.register(models.IP,IPAdmin)
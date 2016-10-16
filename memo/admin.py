from django.contrib import admin
import models
# Register your models here.
class Admin(admin.ModelAdmin):
    list_display = ('body', )

admin.site.register(models.Memo,Admin)
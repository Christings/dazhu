from django.contrib import admin
import models
# Register your models here.
class Admin(admin.ModelAdmin):
    list_display = ('title', 'author',)

admin.site.register(models.Memo,Admin)
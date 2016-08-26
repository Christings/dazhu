from django.contrib import admin
from models import CmsItem
# Register your models here.
class CmsAdmin(admin.ModelAdmin):
    list_display = ('title', 'controller', "view","itemID",)
   
        
    
admin.site.register(CmsItem, CmsAdmin)
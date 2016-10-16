from django.contrib import admin
import models
from django.contrib.admin.actions import delete_selected as delete_selected_
# Register your models here.
class PhotoesAdmin(admin.ModelAdmin):
    list_display = ('rndName', 'showName', "phototype" , 'timestamp',)
    
    readonly_fields = ('rndName', 'timestamp',)
    
    actions = ['delete_selected']
    def delete_selected(self, request, obj):
        for o in obj.all():            
            o.delete()
        return delete_selected_(self, request, obj)
        
        
    
admin.site.register(models.Photoes, PhotoesAdmin)

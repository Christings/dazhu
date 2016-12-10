from django.contrib import admin
import models
from django import forms
# Register your models here.


class AttachmentAdminForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    sourceName = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    rndName = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = models.attachment
        fields = ["title","rndName","sourceName"]

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'sourceName','rndName',)
    #readonly_fields = ('title',)
    actions = ['delete_selected']
    def delete_selected(self, request, obj):
        for o in obj.all():            
            o.delete()
        return delete_selected_(self, request, obj)
        
    def get_title(self, obj):
        return obj.blog.title
    
    def get_form(self, request, obj=None, *args, **kwargs):
        #form = super(AttachmentAdmin, self).get_form(request, *args, **kwargs)
        
        form = AttachmentAdminForm
        print(kwargs)
        # Initial values
        if obj and obj.blog:
            form.base_fields['title'].initial = obj.blog.title
            form.base_fields['sourceName'].initial = obj.sourceName
            form.base_fields['rndName'].initial = obj.rndName
        return form
    
    
    
    
admin.site.register(models.attachment,AttachmentAdmin)
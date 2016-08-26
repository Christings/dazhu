from django.contrib import admin

from models import Diary
import tools.webTools as tools
from django.http import HttpResponse
# Register your models here.

class DiaryAdmin(admin.ModelAdmin):
    list_display = ('weather','author','timestamp')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            tempDiary = Diary.objects.get(id=object_id)
            tools.debug("obj id ",object_id)
            tools.debug("author id",tempDiary.author.id)
            tools.debug("request author id",request.user.id)
            if tempDiary.author.id != request.user.id or \
                            "user_login" not in request.session:
                tools.debug("change diary error")
                return HttpResponse("cannot access this diary")            
        except:
            tools.debug("change diary except error")
            pass        

        return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)

admin.site.register(Diary,DiaryAdmin)

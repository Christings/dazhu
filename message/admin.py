from django.contrib import admin
from models import Message
# Register your models here.
class Message_admin(admin.ModelAdmin):
    list_display = ('guid', 'author', "timestamp","body",)

admin.site.register(Message, Message_admin)
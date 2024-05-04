from django.contrib import admin
from .models import ChatBox, Message


class MessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender', 'receiver', 'content', 'is_read']


admin.site.register(ChatBox)
admin.site.register(Message, MessageAdmin)

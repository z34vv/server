from django.contrib import admin
from .models import Post, Comment, Hashtag


class PostAdmin(admin.ModelAdmin):
    list_editable = ['view_mode', 'chat_mode',]
    list_display = ['post_id', 'author', 'view_mode', 'chat_mode', 'created_at']


class HashtagAdmin(admin.ModelAdmin):
    list_display = ['name', 'times_of_use']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_id', 'author', 'post', 'created_at']


admin.site.register(Post, PostAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Comment, CommentAdmin)

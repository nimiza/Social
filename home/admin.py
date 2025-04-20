from django.contrib import admin
from .models import Post, Comment, Vote


class PostAdmin(admin.ModelAdmin):
    fields = [("user", "slug"), "body"]
    list_display = ["slug", "user", "updated"]
    prepopulated_fields = {'slug':["body"]}
    raw_id_fields = ["user"]
    search_fields = ["body"]
    list_filter = ["updated", "created"]


class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'post', 'replied_to']
    fields = [("user", "post", "replied_to"), "body", "is_reply"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote)
from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publication_date', 'status']
    list_filter = ['status', 'created_date', 'publication_date', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publication_date'
    ordering = ['status', '-publication_date']
    list_editable = ['status']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_author_name', 'post', 'created_date', 'active']
    list_filter = ['active', 'created_date']
    search_fields = ['guest_name', 'guest_email', 'text']
    actions = ['approve_comments']
    
    def get_author_name(self, obj):
        return obj.get_author_name()
    get_author_name.short_description = 'Author'
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
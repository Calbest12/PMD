from django.contrib import admin
from .models import Project, Comment, ProjectHistory

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'created_by', 'progress', 'deadline', 'is_overdue']
    list_filter = ['status', 'priority', 'created_at', 'deadline']
    search_fields = ['title', 'description']
    filter_horizontal = ['assigned_users']
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['project', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['project__title', 'author__username', 'text']

@admin.register(ProjectHistory)
class ProjectHistoryAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'action', 'timestamp']
    list_filter = ['timestamp', 'action']
    search_fields = ['project__title', 'user__username', 'action']
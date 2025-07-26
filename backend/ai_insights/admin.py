from django.contrib import admin
from .models import AIInsight, AITrainingData, ChatInteraction

@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_user', 'insight_type', 'confidence_score', 'applied', 'dismissed', 'created_at']
    list_filter = ['insight_type', 'applied', 'dismissed', 'created_at']
    search_fields = ['title', 'content', 'target_user__username']
    readonly_fields = ['created_at']

@admin.register(AITrainingData)
class AITrainingDataAdmin(admin.ModelAdmin):
    list_display = ['uploaded_by', 'category', 'status', 'timestamp']
    list_filter = ['category', 'status', 'timestamp']
    search_fields = ['text_input', 'uploaded_by__username']

@admin.register(ChatInteraction)
class ChatInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'message', 'response']
    readonly_fields = ['created_at']
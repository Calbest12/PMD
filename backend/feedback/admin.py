from django.contrib import admin
from .models import SliderFeedback, PerformanceMetric

@admin.register(SliderFeedback)
class SliderFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'category', 'score', 'submitted_at']
    list_filter = ['category', 'score', 'submitted_at']
    search_fields = ['user__username', 'project__title']

@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ['project', 'metric_type', 'value', 'unit', 'updated_by', 'updated_at']
    list_filter = ['metric_type', 'updated_at']
    search_fields = ['project__title']

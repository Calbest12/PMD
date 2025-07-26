from django.contrib import admin
from .models import CareerDevelopmentForm

@admin.register(CareerDevelopmentForm)
class CareerDevelopmentFormAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_name', 'category', 'current_level', 'target_level', 'priority', 'target_date']
    list_filter = ['category', 'priority', 'current_level', 'target_level']
    search_fields = ['user__username', 'skill_name']
    readonly_fields = ['submitted_at', 'updated_at']

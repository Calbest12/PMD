from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from projects.models import Project


class SliderFeedback(models.Model):
    CATEGORY_CHOICES = [
        ('PM', 'Project Management'),
        ('ChangeMgmt', 'Change Management'),
        ('Leadership', 'Leadership'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='slider_feedback')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'project', 'category']
        ordering = ['-submitted_at']


class PerformanceMetric(models.Model):
    METRIC_TYPES = [
        ('progress', 'Project Progress'),
        ('performance', 'Team Performance'),
        ('budget', 'Budget Utilization'),
        ('quality', 'Code Quality'),
        ('satisfaction', 'Client Satisfaction'),
        ('timeline', 'Timeline Adherence'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='metrics')
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.FloatField()
    unit = models.CharField(max_length=10, default='%')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['project', 'metric_type']
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from projects.models import Project


class AITrainingData(models.Model):
    CATEGORY_CHOICES = [
        ('leadership', 'Leadership'),
        ('project_management', 'Project Management'),
        ('self_knowledge', 'Self Knowledge'),
        ('market_knowledge', 'Market Knowledge'),
    ]

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    text_input = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')


class AIInsight(models.Model):
    INSIGHT_TYPES = [
        ('feedback', 'Feedback'),
        ('suggestion', 'Suggestion'),
        ('recommendation', 'Recommendation'),
        ('performance', 'Performance'),
        ('risk', 'Risk'),
        ('opportunity', 'Opportunity'),
        ('trend', 'Trend'),
    ]

    related_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='ai_insights')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_insights')

    title = models.CharField(max_length=200)
    content = models.TextField()
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPES)
    confidence_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    # Metadata
    category = models.CharField(max_length=50, blank=True)
    applied = models.BooleanField(default=False)
    dismissed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ChatInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    context = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
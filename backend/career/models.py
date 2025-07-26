from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class CareerDevelopmentForm(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('management', 'Management'),
        ('communication', 'Communication'),
        ('design', 'Design'),
        ('analytics', 'Analytics'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # User and basic info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='career_forms')
    skill_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # Skill levels
    current_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    target_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    current_progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Timeline and priority
    target_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # Additional details
    notes = models.TextField(blank=True)
    resources = models.JSONField(default=list, blank=True)  # List of learning resources

    # Review information
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='reviewed_forms')
    manager_notes = models.TextField(blank=True)

    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.skill_name}"

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.target_date < timezone.now().date()
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('team_member', 'Team Member'),
        ('manager', 'Manager'),
        ('executive_leader', 'Executive Leader'),
        ('ai_lead', 'AI Lead'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='team_member')
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional profile fields
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    @property
    def full_name(self):
        return self.get_full_name() or self.username


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    color = models.CharField(max_length=7, default='#3b82f6')  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
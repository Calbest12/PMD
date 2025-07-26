from rest_framework import status, viewsets, permissions
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import User
from .models import CareerDevelopmentForm
from .serializers import CareerDevelopmentFormSerializer


class CareerDevelopmentFormViewSet(viewsets.ModelViewSet):
    serializer_class = CareerDevelopmentFormSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'priority', 'current_level', 'target_level']
    search_fields = ['skill_name', 'notes']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            # Managers can see their team members' forms
            team_members = User.objects.filter(
                assigned_projects__created_by=user
            ).distinct()
            return CareerDevelopmentForm.objects.filter(
                Q(user=user) | Q(user__in=team_members)
            )
        elif user.role == 'executive_leader':
            return CareerDevelopmentForm.objects.all()
        else:
            return CareerDevelopmentForm.objects.filter(user=user)

    def perform_create(self, serializer):
        career_form = serializer.save(user=self.request.user)
        # Generate AI insight for career development
        from ai_insights.utils import generate_career_ai_insight
        generate_career_ai_insight(self.request.user, career_form)
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from django.utils import timezone
import json

from projects.models import Project
from .models import SliderFeedback, PerformanceMetric
from .serializers import SliderFeedbackSerializer, PerformanceMetricSerializer


# Feedback ViewSet
class SliderFeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = SliderFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role in ['manager', 'executive_leader']:
            return SliderFeedback.objects.all()
        return SliderFeedback.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_slider_feedback(request):
    project_id = request.data.get('project_id')
    category = request.data.get('category')
    score = request.data.get('score')

    try:
        project = Project.objects.get(id=project_id)

        # Check if user has access to this project
        if (request.user.role == 'team_member' and
                request.user not in project.assigned_users.all()):
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

        # Update or create feedback
        feedback, created = SliderFeedback.objects.update_or_create(
            user=request.user,
            project=project,
            category=category,
            defaults={'score': score}
        )

        # Generate AI insight
        from ai_insights.utils import generate_ai_insight
        generate_ai_insight(request.user, project, category, score)

        return Response({
            'message': 'Feedback updated successfully',
            'created': created
        })

    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Performance Metrics ViewSet
class PerformanceMetricViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project', None)
        queryset = PerformanceMetric.objects.all()

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        # Filter based on user role and project access
        if self.request.user.role == 'team_member':
            accessible_projects = self.request.user.assigned_projects.all()
            queryset = queryset.filter(project__in=accessible_projects)

        return queryset

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)


# Dashboard Analytics
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_analytics(request):
    user = request.user

    # Get user's accessible projects
    if user.role == 'executive_leader':
        projects = Project.objects.all()
    elif user.role == 'manager':
        projects = Project.objects.filter(
            Q(created_by=user) | Q(assigned_users=user)
        ).distinct()
    else:
        projects = Project.objects.filter(assigned_users=user)

    # Calculate analytics
    total_projects = projects.count()
    active_projects = projects.filter(status='active').count()
    completed_projects = projects.filter(status='completed').count()
    overdue_projects = sum(1 for p in projects if p.is_overdue)

    # Average scores
    avg_scores = {}
    for category in ['PM', 'ChangeMgmt', 'Leadership']:
        avg_score = SliderFeedback.objects.filter(
            project__in=projects,
            category=category
        ).aggregate(avg=Avg('score'))['avg']
        avg_scores[category] = round(avg_score or 0, 1)

    # Recent AI insights
    from ai_insights.models import AIInsight
    from ai_insights.serializers import AIInsightSerializer
    recent_insights = AIInsight.objects.filter(
        Q(target_user=user) | Q(related_project__in=projects)
    ).filter(dismissed=False)[:5]

    return Response({
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'overdue_projects': overdue_projects,
        'completion_rate': round((completed_projects / total_projects * 100) if total_projects > 0 else 0, 1),
        'average_scores': avg_scores,
        'recent_insights': AIInsightSerializer(recent_insights, many=True).data,
    })
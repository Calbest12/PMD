from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
import logging

from accounts.models import User
from projects.models import Project
from .models import AIInsight, AITrainingData, ChatInteraction
from .serializers import AIInsightSerializer, ChatSerializer
from .utils import call_storai_api

logger = logging.getLogger(__name__)


# AI Insights ViewSet
class AIInsightViewSet(viewsets.ModelViewSet):
    serializer_class = AIInsightSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['insight_type', 'category', 'applied', 'dismissed']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'executive_leader':
            return AIInsight.objects.all()
        elif user.role == 'manager':
            # Managers see insights for their projects and team members
            managed_projects = Project.objects.filter(created_by=user)
            team_members = User.objects.filter(assigned_projects__in=managed_projects).distinct()
            return AIInsight.objects.filter(
                Q(target_user=user) |
                Q(target_user__in=team_members) |
                Q(related_project__in=managed_projects)
            ).distinct()
        else:
            return AIInsight.objects.filter(target_user=user)

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        insight = self.get_object()
        insight.applied = True
        insight.save()
        return Response({'message': 'Insight applied successfully'})

    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        insight = self.get_object()
        insight.dismissed = True
        insight.save()
        return Response({'message': 'Insight dismissed'})


# AI Chat Endpoint
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ai_chat(request):
    serializer = ChatSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    message = serializer.validated_data['message']
    context = serializer.validated_data.get('context', {})

    try:
        # Call AI service
        ai_response = call_storai_api(message, context, request.user)

        # Log the interaction
        ChatInteraction.objects.create(
            user=request.user,
            message=message,
            response=ai_response,
            context=context
        )

        return Response({
            'response': ai_response,
            'timestamp': timezone.now().isoformat()
        })

    except Exception as e:
        logger.error(f"AI Chat error for user {request.user.id}: {str(e)}")
        return Response({
            'error': 'AI service temporarily unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import User
from .models import Project, Comment
from .serializers import ProjectSerializer, ProjectCreateSerializer, CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'team']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'deadline', 'priority']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'executive_leader':
            return Project.objects.all()
        elif user.role == 'manager':
            return Project.objects.filter(
                Q(created_by=user) | Q(assigned_users=user)
            ).distinct()
        else:
            return Project.objects.filter(assigned_users=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            project.assigned_users.add(user)
            return Response({'message': f'{user.get_full_name()} added to project'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            project.assigned_users.remove(user)
            return Response({'message': f'{user.get_full_name()} removed from project'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

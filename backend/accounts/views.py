from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.models import Q
import logging

from .models import User, Team
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, TeamSerializer

logger = logging.getLogger(__name__)


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    print(f"Login request data: {request.data}")  # Debug print

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    print(f"Serializer errors: {serializer.errors}")  # Debug print
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        # Here you would typically send an email with reset link
        # For now, we'll just return success
        logger.info(f"Password reset requested for {email}")
        return Response({'message': 'If that email exists, you\'ll get a reset link shortly.'})
    except User.DoesNotExist:
        # Don't reveal if email exists or not
        return Response({'message': 'If that email exists, you\'ll get a reset link shortly.'})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    # In production, you'd validate the reset token here
    new_password = request.data.get('new_password')

    if not new_password:
        return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

    # For demo purposes, we'll just return success
    return Response({'message': 'Password has been reset successfully'})


# User ViewSet
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# Team ViewSet
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'executive_leader':
            return Team.objects.all()
        return Team.objects.filter(
            Q(leader=self.request.user) | Q(members=self.request.user)
        ).distinct()
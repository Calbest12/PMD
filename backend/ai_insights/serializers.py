from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import AIInsight, AITrainingData, ChatInteraction


class AIInsightSerializer(serializers.ModelSerializer):
    target_user = UserSerializer(read_only=True)
    related_project = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AIInsight
        fields = '__all__'


class AITrainingDataSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = AITrainingData
        fields = '__all__'


class ChatSerializer(serializers.Serializer):
    message = serializers.CharField()
    context = serializers.JSONField(required=False, default=dict)
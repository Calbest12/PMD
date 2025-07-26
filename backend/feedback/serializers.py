from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import SliderFeedback, PerformanceMetric


class SliderFeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SliderFeedback
        fields = '__all__'


class PerformanceMetricSerializer(serializers.ModelSerializer):
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = PerformanceMetric
        fields = '__all__'
from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import CareerDevelopmentForm


class CareerDevelopmentFormSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = CareerDevelopmentForm
        fields = '__all__'
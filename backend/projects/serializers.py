from rest_framework import serializers
from accounts.serializers import UserSerializer, TeamSerializer
from .models import Project, Comment, ProjectHistory


class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_users = UserSerializer(many=True, read_only=True)
    team = TeamSerializer(read_only=True)
    average_scores = serializers.SerializerMethodField()
    ai_insights_count = serializers.SerializerMethodField()
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_average_scores(self, obj):
        return {
            'PM': round(obj.get_average_score('PM'), 1),
            'ChangeMgmt': round(obj.get_average_score('ChangeMgmt'), 1),
            'Leadership': round(obj.get_average_score('Leadership'), 1),
        }

    def get_ai_insights_count(self, obj):
        return obj.ai_insights.filter(dismissed=False).count()


class ProjectCreateSerializer(serializers.ModelSerializer):
    assigned_user_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    team_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'priority', 'deadline',
                  'assigned_user_ids', 'team_id']

    def create(self, validated_data):
        assigned_user_ids = validated_data.pop('assigned_user_ids', [])
        team_id = validated_data.pop('team_id', None)

        project = Project.objects.create(**validated_data)

        if assigned_user_ids:
            project.assigned_users.set(assigned_user_ids)

        if team_id:
            try:
                from accounts.models import Team
                team = Team.objects.get(id=team_id)
                project.team = team
                project.save()
            except Team.DoesNotExist:
                pass

        return project


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
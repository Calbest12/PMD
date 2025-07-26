from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Create users
        users = []

        # Create executive
        executive, created = User.objects.get_or_create(
            username='executive',
            defaults={
                'email': 'executive@company.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'role': 'executive_leader'
            }
        )
        if created:
            executive.set_password('password123')
            executive.save()
        users.append(executive)

        # Create managers
        for i in range(2):
            manager, created = User.objects.get_or_create(
                username=f'manager{i + 1}',
                defaults={
                    'email': f'manager{i + 1}@company.com',
                    'first_name': ['Mike', 'Alice'][i],
                    'last_name': ['Chen', 'Rodriguez'][i],
                    'role': 'manager'
                }
            )
            if created:
                manager.set_password('password123')
                manager.save()
            users.append(manager)

        # Create team members
        team_member_data = [
            ('john_doe', 'john@company.com', 'John', 'Doe'),
            ('jane_smith', 'jane@company.com', 'Jane', 'Smith'),
            ('bob_wilson', 'bob@company.com', 'Bob', 'Wilson'),
            ('emily_davis', 'emily@company.com', 'Emily', 'Davis'),
        ]

        for username, email, first_name, last_name in team_member_data:
            member, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'team_member'
                }
            )
            if created:
                member.set_password('password123')
                member.save()
            users.append(member)

        # Create teams
        from accounts.models import Team
        team1, created = Team.objects.get_or_create(
            name='Frontend Team',
            defaults={
                'description': 'Frontend development team',
                'leader': users[1],  # manager1
                'color': '#3b82f6'
            }
        )
        if created:
            team1.members.set(users[3:5])  # Add some team members

        team2, created = Team.objects.get_or_create(
            name='Backend Team',
            defaults={
                'description': 'Backend development team',
                'leader': users[2],  # manager2
                'color': '#10b981'
            }
        )
        if created:
            team2.members.set(users[5:7])  # Add some team members

        # Create projects
        from projects.models import Project
        projects_data = [
            {
                'title': 'E-commerce Platform Redesign',
                'description': 'Complete overhaul of the e-commerce platform with modern UI/UX',
                'status': 'active',
                'priority': 'high',
                'progress': 75,
                'team': team1,
                'deadline': date.today() + timedelta(days=45)
            },
            {
                'title': 'API Infrastructure Upgrade',
                'description': 'Migrate to microservices architecture and improve API performance',
                'status': 'active',
                'priority': 'critical',
                'progress': 60,
                'team': team2,
                'deadline': date.today() + timedelta(days=30)
            },
            {
                'title': 'Mobile App Development',
                'description': 'Native mobile application for iOS and Android',
                'status': 'planning',
                'priority': 'medium',
                'progress': 25,
                'team': team1,
                'deadline': date.today() + timedelta(days=90)
            }
        ]

        for project_data in projects_data:
            team = project_data.pop('team')
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={
                    **project_data,
                    'created_by': team.leader,
                    'team': team
                }
            )
            if created:
                project.assigned_users.set(team.members.all())

        # Create sample feedback
        from feedback.models import SliderFeedback
        projects = Project.objects.all()
        categories = ['PM', 'Leadership', 'ChangeMgmt']

        for project in projects:
            for user in project.assigned_users.all():
                for category in categories:
                    SliderFeedback.objects.get_or_create(
                        user=user,
                        project=project,
                        category=category,
                        defaults={'score': random.randint(4, 7)}
                    )

        # Create sample career development forms
        from career.models import CareerDevelopmentForm
        skills_data = [
            ('Vue.js Advanced Patterns', 'technical', 'intermediate', 'advanced'),
            ('Team Leadership', 'management', 'beginner', 'intermediate'),
            ('System Architecture', 'technical', 'advanced', 'expert'),
            ('Public Speaking', 'communication', 'beginner', 'intermediate'),
        ]

        for i, (skill, category, current, target) in enumerate(skills_data):
            if i < len(users) - 2:  # Avoid executives and some managers
                user = users[i + 2]
                CareerDevelopmentForm.objects.get_or_create(
                    user=user,
                    skill_name=skill,
                    defaults={
                        'category': category,
                        'current_level': current,
                        'target_level': target,
                        'current_progress': random.randint(20, 80),
                        'target_date': date.today() + timedelta(days=random.randint(60, 180)),
                        'priority': random.choice(['medium', 'high']),
                        'notes': f'Focused learning plan for {skill} development',
                        'resources': [
                            {'name': f'{skill} Documentation', 'url': 'https://example.com'},
                            {'name': f'{skill} Tutorial', 'url': 'https://tutorial.com'}
                        ]
                    }
                )

        # Create sample AI insights
        from ai_insights.models import AIInsight
        insights_data = [
            {
                'title': 'Project Timeline Optimization',
                'content': 'Based on current progress metrics, consider reallocating resources to critical path items to meet the deadline.',
                'insight_type': 'suggestion',
                'category': 'project_management'
            },
            {
                'title': 'Team Collaboration Enhancement',
                'content': 'Leadership scores indicate strong potential. Consider implementing peer mentoring to leverage your strengths.',
                'insight_type': 'recommendation',
                'category': 'leadership'
            },
            {
                'title': 'Skill Development Opportunity',
                'content': 'Your technical growth trajectory suggests readiness for advanced architecture training.',
                'insight_type': 'opportunity',
                'category': 'career'
            }
        ]

        projects = Project.objects.all()
        for i, insight_data in enumerate(insights_data):
            if i < len(projects):
                AIInsight.objects.get_or_create(
                    title=insight_data['title'],
                    defaults={
                        **insight_data,
                        'related_project': projects[i],
                        'target_user': projects[i].assigned_users.first(),
                        'confidence_score': random.uniform(0.7, 0.9)
                    }
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Sample users created:')
        self.stdout.write('- executive@company.com (password: password123)')
        self.stdout.write('- manager1@company.com (password: password123)')
        self.stdout.write('- manager2@company.com (password: password123)')
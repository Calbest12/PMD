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
                username=f'manager{i+1}',
                defaults={
                    'email': f'manager{i+1}@company.com',
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
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Sample users created:')
        self.stdout.write('- executive@company.com (password: password123)')
        self.stdout.write('- manager1@company.com (password: password123)')
        self.stdout.write('- manager2@company.com (password: password123)')
        self.stdout.write('- john@company.com (password: password123)')
        self.stdout.write('- jane@company.com (password: password123)')
        self.stdout.write('- bob@company.com (password: password123)')
        self.stdout.write('- emily@company.com (password: password123)')

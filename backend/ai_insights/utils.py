from django.utils import timezone
import requests
import json
import random
import logging

from .models import AIInsight

logger = logging.getLogger(__name__)


def call_storai_api(message, context, user):
    """
    Call StorAI API for chat responses
    Replace this with your actual StorAI integration
    """
    try:
        # Mock implementation - replace with actual API call
        mock_responses = [
            f"Based on your role as {user.get_role_display()}, I recommend focusing on strategic communication with your team.",
            "Your recent feedback patterns suggest strong technical skills. Consider developing leadership capabilities to complement your expertise.",
            "The project metrics indicate good progress. I suggest implementing regular check-ins to maintain momentum.",
            "Your career development goals align well with current market demands. Focus on practical application of new skills.",
            "Team collaboration scores show room for improvement. Consider organizing team-building activities.",
            f"Hello {user.first_name}! I'm here to help with leadership development and project management insights.",
        ]

        # Select response based on context
        if 'leadership' in message.lower():
            response = "For leadership development, focus on active listening, clear communication, and empowering team members. Consider setting up regular one-on-ones."
        elif 'project' in message.lower():
            response = "For effective project management, ensure clear milestones, regular stakeholder communication, and proactive risk management."
        elif 'career' in message.lower():
            response = "Career growth requires continuous learning, networking, and seeking feedback. Set specific, measurable goals for skill development."
        else:
            response = random.choice(mock_responses)

        return response

    except Exception as e:
        logger.error(f"StorAI API error: {str(e)}")
        return "I'm having trouble connecting to my knowledge base right now. Please try again later."


def generate_ai_insight(user, project, category, score):
    """Generate AI insight based on slider feedback"""
    try:
        # Determine insight based on score and category
        insights = {
            'PM': {
                'high': f"Excellent project management score of {score}/7! Your organizational skills are contributing to project success.",
                'medium': f"Good project management progress with {score}/7. Consider focusing on timeline optimization and stakeholder communication.",
                'low': f"Project management score of {score}/7 shows room for improvement. I recommend reviewing task prioritization and delegation strategies."
            },
            'Leadership': {
                'high': f"Outstanding leadership rating of {score}/7! Your team guidance and decision-making are highly effective.",
                'medium': f"Solid leadership score of {score}/7. Focus on developing team motivation and conflict resolution skills.",
                'low': f"Leadership score of {score}/7 indicates growth opportunities. Consider mentorship programs and leadership training."
            },
            'ChangeMgmt': {
                'high': f"Excellent change management score of {score}/7! Your adaptability is a key strength.",
                'medium': f"Good change management with {score}/7. Work on proactive communication during transitions.",
                'low': f"Change management score of {score}/7 suggests focusing on flexibility and stakeholder buy-in strategies."
            }
        }

        # Determine performance level
        if score >= 6:
            level = 'high'
            insight_type = 'feedback'
        elif score >= 4:
            level = 'medium'
            insight_type = 'suggestion'
        else:
            level = 'low'
            insight_type = 'recommendation'

        suggestion_text = insights.get(category, {}).get(level, f"Score of {score}/7 recorded for {category}")

        AIInsight.objects.create(
            related_project=project,
            target_user=user,
            title=f"{category} Performance Insight",
            content=suggestion_text,
            insight_type=insight_type,
            confidence_score=0.8,
            category=category.lower()
        )

    except Exception as e:
        logger.error(f"Error generating AI insight: {str(e)}")


def generate_career_ai_insight(user, career_form):
    """Generate AI insight for career development"""
    try:
        skill_gap = ['beginner', 'intermediate', 'advanced', 'expert'].index(career_form.target_level) - \
                    ['beginner', 'intermediate', 'advanced', 'expert'].index(career_form.current_level)

        if skill_gap == 1:
            suggestion = f"Your goal to advance from {career_form.current_level} to {career_form.target_level} in {career_form.skill_name} is achievable. Focus on hands-on practice and seeking mentorship."
        elif skill_gap == 2:
            suggestion = f"Advancing two levels in {career_form.skill_name} is ambitious but possible. Consider breaking this into intermediate milestones and allocating additional time for practice."
        else:
            suggestion = f"Your {career_form.skill_name} development plan shows strong ambition. Create a structured learning path with regular checkpoints to track progress."

        AIInsight.objects.create(
            target_user=user,
            title=f"Career Development: {career_form.skill_name}",
            content=suggestion,
            insight_type='recommendation',
            confidence_score=0.7,
            category='career_development'
        )

    except Exception as e:
        logger.error(f"Error generating career AI insight: {str(e)}")

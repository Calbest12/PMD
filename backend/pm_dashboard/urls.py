"""
URL configuration for pm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

# Import views from apps
from accounts import views as auth_views
from feedback import views as feedback_views
from ai_insights import views as ai_views

# API Router
router = DefaultRouter()
router.register(r'users', auth_views.UserViewSet)
router.register(r'teams', auth_views.TeamViewSet)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('api/auth/register/', auth_views.register, name='register'),
    path('api/auth/login/', auth_views.login, name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/forgot-password/', auth_views.forgot_password, name='forgot_password'),
    path('api/auth/reset-password/', auth_views.reset_password, name='reset_password'),

    # API Routes
    path('api/', include(router.urls)),
    path('api/projects/', include('projects.urls')),
    path('api/feedback/', include('feedback.urls')),
    path('api/career-development/', include('career.urls')),
    path('api/ai/', include('ai_insights.urls')),

    # Custom endpoints
    path('api/dashboard/analytics/', feedback_views.dashboard_analytics, name='dashboard_analytics'),
]


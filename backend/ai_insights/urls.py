from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'insights', views.AIInsightViewSet, basename='ai-insights')

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', views.ai_chat, name='ai_chat'),
]

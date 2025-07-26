from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'slider-feedback', views.SliderFeedbackViewSet, basename='slider-feedback')
router.register(r'metrics', views.PerformanceMetricViewSet, basename='performance-metrics')

urlpatterns = [
    path('', include(router.urls)),
    path('slider/', views.submit_slider_feedback, name='submit_slider_feedback'),
]

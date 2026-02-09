from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lessons.views import LessonViewSet

router = DefaultRouter()
router.register('lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('api/', include(router.urls)),
]

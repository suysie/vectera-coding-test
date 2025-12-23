from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeetingViewSet

router = DefaultRouter()
router.register(r"meetings", MeetingViewSet, basename="meeting")

urlpatterns = [
    path("", include(router.urls)),
    path("meetings/<int:pk>/notes/", MeetingViewSet.as_view({'get': 'list_notes'}), name='meeting-notes-list'),
]

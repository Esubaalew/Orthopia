from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet
from . import views
from django.urls import include


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path("", views.index),
    path("api/", include(router.urls)),
]

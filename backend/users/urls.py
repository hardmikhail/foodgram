from rest_framework.routers import DefaultRouter
from django.urls import path, include


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
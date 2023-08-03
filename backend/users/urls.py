from rest_framework.routers import DefaultRouter
from django.urls import path, include


app_name = 'users'
router = DefaultRouter()


urlpatterns = [
    # path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
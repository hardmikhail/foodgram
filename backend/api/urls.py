from rest_framework.routers import DefaultRouter
from django.urls import path, include
from djoser.views import UserViewSet
from .views import (
    TagsVeiwSet,
    IngredientsViewSet,
    RecipesVeiwSet,
    SubscribeViewSet,
    FavoriteViewSet,
)

app_name = 'api'
router = DefaultRouter()
router.register(r'tags', TagsVeiwSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'recipes', RecipesVeiwSet)
router.register(r'recipes', FavoriteViewSet)
router.register(r'users', SubscribeViewSet)
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

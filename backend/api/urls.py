from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TagsVeiwSet,
    IngredientsViewSet,
    RecipesVeiwSet,
    SubscribeViewSet
)

app_name = 'api'
router = DefaultRouter()
router.register(r'tags', TagsVeiwSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'recipes', RecipesVeiwSet)
router.register(r'users', SubscribeViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

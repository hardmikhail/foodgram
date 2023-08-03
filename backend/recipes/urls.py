from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import TagsVeiwSet, IngredientsViewSet, RecipesVeiwSet

app_name = 'recipes'
router = DefaultRouter()
router.register(r'tags', TagsVeiwSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'recipes', RecipesVeiwSet)




urlpatterns = [
    path('', include(router.urls)),
]
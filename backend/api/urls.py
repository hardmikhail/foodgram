from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TagsVeiwSet, IngredientsViewSet, RecipesVeiwSet, ShoppingCartViewSet, SubscribeViewSet

app_name = 'api'
router = DefaultRouter()
router.register(r'tags', TagsVeiwSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'recipes', RecipesVeiwSet)
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet)
# router.register(r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet)
router.register(r'users', SubscribeViewSet, basename='sub')
router.register(r'users/subscriptions', SubscribeViewSet)




urlpatterns = [
    path('', include(router.urls)),
]
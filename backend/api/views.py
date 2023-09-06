from django.http import HttpResponse
from rest_framework import viewsets, status, response, filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend

from api.pagination import CustomPagination
from .filters import RecipeFilter
from .permissions import CustomUsers, CustomAuthor
from users.models import Subscribe
from . import serializers
from django.contrib.auth import get_user_model
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    ShoppingCart,
    RecipeIngredient
)

User = get_user_model()


class TagsVeiwSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagsSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = serializers.IngredientsSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipesVeiwSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (CustomAuthor,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return serializers.RecipesPOSTSerializer
        return serializers.RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    permission_classes = (CustomAuthor,)
    serializer_class = serializers.RecipeShortSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(id=pk)
        if request.method == 'POST':
            Favorite.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = serializers.RecipeShortSerializer(
                recipe,
                context={'request': request}
            )
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        favorite = Favorite.objects.filter(
            user=user,
            recipe=recipe
        )
        if favorite.exists():
            favorite.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        raise ValidationError('Избранное не найдено!')


class ShoppingCartViewSet(viewsets.GenericViewSet):
    queryset = ShoppingCart.objects.all()
    permission_classes = (CustomAuthor,)
    serializer_class = serializers.RecipeShortSerializer

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(id=pk)
        if request.method == 'POST':
            ShoppingCart.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = serializers.RecipeShortSerializer(
                recipe,
                context={'request': request}
            )
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        shopping_cart = ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        )
        if shopping_cart.exists():
            shopping_cart.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        raise ValidationError('Список покупок не найден!')

    @action(detail=False)
    def download_shopping_cart(self, request):
        shopping_list = 'Список покупок'
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=request.user)
            .order_by('ingredient__name')
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
        )
        for ingredient in ingredients:
            shopping_list += (
                f'\n{ingredient["ingredient__name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}'
            )
        return HttpResponse(shopping_list, content_type='text/plain')


class SubscribeViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (CustomUsers,)

    @action(detail=False)
    def subscriptions(self, request):
        subscriptions = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(subscriptions)
        serializer = serializers.SubscribeSerializer(
            pages,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        user = self.request.user
        following = User.objects.get(id=pk)
        if request.method == 'POST':
            if Subscribe.objects.filter(
                user=user,
                following=following
            ).exists():
                raise ValidationError('Подписка уже оформлена!')
            if User.objects.get(id=pk) == self.request.user:
                raise ValidationError('Нельзя подписаться на самого себя!')
            Subscribe.objects.create(
                user=user,
                following=following
            )
            serializer = serializers.SubscribeSerializer(
                following,
                context={'request': request}
            )
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            subscribe = Subscribe.objects.filter(
                user=user,
                following=following
            )
            if subscribe.exists():
                subscribe.delete()
                return response.Response(status=status.HTTP_204_NO_CONTENT)
            raise ValidationError('Подписка не найдена!')

from django.shortcuts import render, get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins, viewsets, status, response, generics
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from rest_framework.views import APIView
from djoser.views import UserViewSet

from users.models import User
from recipes.models import Tag, Ingredient, Recipe, Subscribe
from .serializers import (TagsSerializer, IngredientsSerializer, RecipeSerializer, RecipesPOSTSerializer, SubscribeSerializer)


class TagsVeiwSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientsSerializer


class RecipesVeiwSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    page_size = 10
    

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipesPOSTSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShoppingCartViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Recipe.objects.all()

class SubscribeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):

    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    # permission_classes = (IsAuthenticated,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('following__username',)
    # @action(methods=['post', 'delete'],
    #         detail=True
    # )
    # def subscribe(self, request, **kwarg):
    #     user = request.user
    #     following = get_object_or_404(User, pk=self.kwargs.get('pk'))
    #     if request.method == 'post':
    #         serializer = SubscribeSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         Subscribe.objects.create(user=user, following=following)
    #         return response.Response(serializer.data)

    # def get_queryset(self):
    #     # print(self.kwargs.get('user_id'))
    #     user = self.request.user
    #     return Subscribe.objects.filter(user=user)

    # def get_object(self, pk):
    #     try:
    #         return Subscribe.objects.get(pk=pk)
    #     except Subscribe.DoesNotExist:
    #         raise ValidationError
    
    # def delete(self, request, pk, format=None):
    #         snippet = self.get_object()
    #         snippet.delete()
    #         return response.Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=False, methods=['post'])
    def perform_create(self, request, **kwarg):
        print(self.kwargs.get('user_id'))
        print(self.request.user)
        print(User.objects.get(id=self.kwargs.get('user_id')))
        if Subscribe.objects.filter(
            user=self.request.user,
            following=User.objects.get(id=self.kwargs.get('user_id'))
        ).exists():
            raise ValidationError('Подписка уже оформлена!')
        if User.objects.get(
                id=self.kwargs.get('user_id')) == self.request.user:
            raise ValidationError('Нельзя подписаться на самого себя!')
        # sub = self.get_object()
        serializer = SubscribeSerializer(data=request.data)
        # if serializer.is_valid():
        #     print(serializer.validated_data)
            # sub.sub(serializer.validated_data['password'])
        serializer.save(
            user = self.request.user,
            following=User.objects.get(id=self.kwargs.get('user_id'))
        )
        return response.Response(serializer.data)
    

    # @action(detail=True, methods=['delete'])
    # def unsub(self, request):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return response.Response(status=status.HTTP_204_NO_CONTENT)
# class SubscribeViewSet:
#     def perform_action(self, user, following, model, response_text):
#         model.objects.create(user=user, following=following)
#         serializer = SubscribeSerializer(following, context={'request': self.request})
#         return response.Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['POST', 'DELETE'])
# def subscribe(request):
#     if request.method == 'POST':
#         serializer = SubscribeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response(serializer.data, status=status.HTTP_201_CREATED)
#         return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubscribeViewSet(UserViewSet):
    @action(detail=False)
    def subscriptions(self, request):
        user = self.request.user
        subscriptions = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(subscriptions)
        serializer = SubscribeSerializer(pages, context={'request': request},many=True)
        # return response.Response(serializer.data, status=status.HTTP_200_OK)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        user = self.request.user
        following=User.objects.get(id=self.kwargs.get('id'))
        serializer = SubscribeSerializer(following, context={'request': request})
        if request.method == 'POST':
            if Subscribe.objects.filter(
                user=user,
                following=User.objects.get(id=self.kwargs.get('id'))
            ).exists():
                raise ValidationError('Подписка уже оформлена!')
            if User.objects.get(
                id=self.kwargs.get('id')) == self.request.user:
                raise ValidationError('Нельзя подписаться на самого себя!')
            Subscribe.objects.create(
                user = self.request.user,
                following=following
            )
            serializer = SubscribeSerializer(following, context={'request': request})
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscribe = Subscribe.objects.filter(
                user=self.request.user,
                following=User.objects.get(id=self.kwargs.get('id'))
            )
            if subscribe.exists():
                subscribe.delete()
                return response.Response(status=status.HTTP_204_NO_CONTENT)
            raise ValidationError('Подписка не найдена!')

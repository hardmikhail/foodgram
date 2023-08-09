# from django.shortcuts import render
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework import mixins, viewsets, status
# from rest_framework.viewsets import GenericViewSet

# from .models import Tag, Ingredient, Recipe
# from .serializers import TagsSerializer, IngredientsSerializer, RecipeSerializer, RecipesPOSTSerializer


# class TagsVeiwSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagsSerializer


# class IngredientsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientsSerializer


# class RecipesVeiwSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     pagination_class = LimitOffsetPagination
#     page_size = 10
    

#     def get_serializer_class(self):
#         if self.action == 'create' or self.action == 'partial_update':
#             return RecipesPOSTSerializer
#         return RecipeSerializer

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
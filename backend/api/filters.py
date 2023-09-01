from django_filters import rest_framework as filters
from django_filters.widgets import CSVWidget

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter()
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = filters.CharFilter(
        distinct=True,
        widget=CSVWidget,
        method='filter_tags'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__slug__in=value)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorite__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset

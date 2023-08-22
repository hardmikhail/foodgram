from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Subscribe,
    Favorite,
    ShoppingCart
)

admin.site.register((Tag, Subscribe, Favorite, ShoppingCart))


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeIngredientAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, ]
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')

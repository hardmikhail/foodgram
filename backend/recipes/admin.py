from django.contrib import admin

from .models import Tag, Ingredient, Recipe, RecipeIngredient, RecipeTag

admin.site.register((Tag, Ingredient, RecipeTag))


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeIngredientAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline,]


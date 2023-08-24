from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


MAX_LENGTH = 200

User = get_user_model()

class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(unique=True, max_length=MAX_LENGTH)
    color = models.CharField(unique=True, max_length=7)
    slug = models.SlugField(unique=True, max_length=MAX_LENGTH)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient'
    )
    name = models.CharField(max_length=MAX_LENGTH)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(max_length=MAX_LENGTH)
    measurement_unit = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель для связи рецептов с ингредиентами."""

    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.recipe.name


class RecipeTag(models.Model):
    """Модель для связи рецептов с тегами."""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe.name


class Favorite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorited'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user} добавил {self.recipe.name} в избранное'


class ShoppingCart(models.Model):
    """Модель корзины покупок."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart'
    )

    def __str__(self):
        return f'{self.user} добавил {self.recipe.name} в список покупок'

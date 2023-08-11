from django.core.files.base import ContentFile
import base64

from rest_framework import serializers, status
from djoser.serializers import UserCreateSerializer
from rest_framework.validators import ValidationError


from users.models import User

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient, Subscribe
from users.serializers import CustomUserSerializer
import webcolors


# class UsersGETSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.BooleanField(default=False)

#     class Meta:
#         fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
#         model = User


# class CustomUserCreateSerializer(UserCreateSerializer):
#     class Meta:
#         fields = ('first_name','last_name', 'username', 'email', 'password')
#         model = User

# class UsersSetPasswordSerializer(serializers.ModelSerializer):

#     class Meta:
#         fields = ('new_password', 'current_password')
#         model = User

class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value
    
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени.')
        return data

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()
    
    class Meta:
        fields = ('id', 
                  'name',
                  'color',
                  'slug')
        model = Tag


class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('__all__')
        model = Ingredient

class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    
    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = RecipeIngredientSerializer(many=True, source='recipe_ingredients')
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipe

class RecipeIngredientPOSTSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

class RecipesPOSTSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientPOSTSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)

# bulk_create
        for ingredient_data in ingredients:
            RecipeIngredient(
                recipe=instance,
                ingredient=ingredient_data['ingredient'],
                amount=ingredient_data['amount']
            ).save()
        return instance
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)

        tags = validated_data.pop('tags')
        lst = []
        for tag in tags:
            current_tag = Tag.objects.get(id=tag.id)
            lst.append(current_tag)
        instance.tags.set(lst)
        instance.ingredients.clear()
        ingredients = validated_data.pop('ingredients')
        for ingredient_data in ingredients:
            RecipeIngredient(
                recipe=instance,
                ingredient=ingredient_data['ingredient'],
                amount=ingredient_data['amount']
            ).save()

        instance.save()
        return instance


        

    def to_representation(self, instance):
        return RecipeSerializer(instance).data

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')
        model = Recipe

class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe

class SubscribeSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # recipes = RecipeShortSerializer(many=True, read_only=True)
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    # email = serializers.ReadOnlyField()
        
    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.follower.filter(following=obj).exists()
    
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
    
    def get_recipes(self,obj):
        return RecipeShortSerializer(Recipe.objects.filter(author=obj), many=True).data
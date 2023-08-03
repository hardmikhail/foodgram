from rest_framework import serializers, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from djoser.serializers import UserCreateSerializer

from users.models import User




class UsersGETSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        model = User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = ('first_name','last_name', 'username', 'email', 'password')
        model = User

class UsersSetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('new_password', 'current_password')
        model = User
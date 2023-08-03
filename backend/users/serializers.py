from djoser.serializers import UserCreateSerializer, TokenCreateSerializer
from rest_framework import serializers

from users.models import User


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        fields = ('email', 'id','username', 'first_name', 'last_name', 'password')
        model = User
        extra_kwargs = {
            'email': {
                'error_messages': {'required': 'Обязательное поле'},
                'required': True
                }, 
            'id': {'read_only': True},
            'username': {'error_messages': {'required': 'Обязательное поле'}},
            'first_name': {
                'error_messages': {'required': 'Обязательное поле'},
                'required': True
                },
            'last_name': {
                'error_messages': {'required': 'Обязательное поле'},
                'required': True
                },
            'password': {
                'error_messages': {'required': 'Обязательное поле'},
                'required': True,
                }, 
        }


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        model = User
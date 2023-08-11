from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from users.models import User


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        fields = ('email', 'id','username', 'first_name', 'last_name', 'password')
        model = User


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    def get_is_subscribed(self, obj):
        try:
            user = self.context.get('request').user
            return user.follower.filter(following=obj).exists()
        except:
            return False
    
    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        model = User
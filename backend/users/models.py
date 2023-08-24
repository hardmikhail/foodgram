from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Subscribe(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
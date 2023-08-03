from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     email = models.EmailField(
#         max_length=254,
#         unique=True,
#     )
User = get_user_model()
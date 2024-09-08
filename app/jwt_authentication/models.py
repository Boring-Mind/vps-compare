from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class JWTToken(models.Model):
    body = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

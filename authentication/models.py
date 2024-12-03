from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    telegram_id = models.CharField(max_length=64, blank=True, null=True)
    telegram_username = models.CharField(max_length=64, blank=True, null=True)


class AuthToken(models.Model):
    token = models.CharField(max_length=64, unique=True)
    session_key = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self) -> bool:
        """Проверяет, истек ли токен."""
        return now() > self.expires_at

    @staticmethod
    def create_token(session_key: str, expiration_minutes: int = 10) -> "AuthToken":
        """Создает новый токен для указанной сессии."""
        import secrets
        return AuthToken.objects.get_or_create(
            token=secrets.token_hex(32),  # Генерация безопасного токена
            session_key=session_key,
            expires_at=now() + timedelta(minutes=expiration_minutes),
        )[0]

    def __str__(self) -> str:
        return self.token

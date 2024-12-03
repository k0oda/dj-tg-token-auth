from django.contrib.auth.backends import BaseBackend
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpRequest

from .models import AuthToken, User


class TelegramBackend(BaseBackend):
    """
    Authenticates using Telegram Bot provided data.
    """

    session_key = "_auth_user_id"
    session_auth_hash_key = "_auth_user_hash"

    def authenticate(self, request: HttpRequest, telegram_id: str, token: str) -> User:
        try:
            auth_token = AuthToken.objects.get(token=token)
            if auth_token and not auth_token.is_expired():
                request.session = SessionStore(session_key=auth_token.session_key)
                user = User.objects.get(telegram_id=telegram_id)
                auth_token.delete()
                return user
        except (User.DoesNotExist, AuthToken.DoesNotExist):
            return None

    def get_user(self, user_id: int) -> User:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

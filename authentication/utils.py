from django.conf import settings
from django.contrib.auth import load_backend, signals
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.http import HttpRequest


def no_session_refresh_login(
        request: HttpRequest,
        user: AbstractBaseUser,
        backend: type[ModelBackend] | str | None = None,
    ) -> None:
    """
    Logs User into a session with no session renewal.
    :param request: request object
    :param user: user to be logged in
    :param backend: authentication backend
    """
    if not user.is_authenticated:
        raise ValueError("User must be authenticated.")

    if backend is None:
        backend = user.backend if hasattr(user, "backend") else None
        if backend is None:
            raise ValueError(
                "You must provide a 'backend' argument or set the 'backend' attribute on the user.",
            )

    backend = load_backend(user.backend)

    request.user = user or AnonymousUser
    request.session["_auth_user_backend"] = user.backend
    request.session[backend.session_key] = user.pk
    request.session[backend.session_auth_hash_key] = user.get_session_auth_hash()

    request.session.save()

    signals.user_logged_in.send(sender=user.__class__, request=request, user=user)


def generate_telegram_link(token: str) -> str:
    telegram_bot_username = settings.TELEGRAM_BOT_USERNAME
    return f"https://t.me/{telegram_bot_username}?start={token}"

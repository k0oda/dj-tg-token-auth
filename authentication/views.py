import json

from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .models import AuthToken
from .utils import generate_telegram_link, no_session_refresh_login


@never_cache
def telegram_login_check(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=404)


@csrf_exempt
def telegram_login(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        telegram_id = data.get("telegram_id")
        username = data.get("telegram_username")
        token = data.get("token")

        if not telegram_id or not username or not token:
            return JsonResponse({"error": "Invalid data"}, status=400)

        user = authenticate(request, telegram_id=telegram_id, token=token)
        if user:
            no_session_refresh_login(request, user)
            return JsonResponse({"message": "Successfully logged in"}, status=200)
        else:
            return JsonResponse({"error": "Invalid token"}, status=401)
    else:
        return JsonResponse({"error": "Bad request"}, status=400)


def index(request: HttpRequest) -> HttpResponse:
    if not request.session.session_key:
        request.session.create()
    token = AuthToken.create_token(request.session.session_key)
    context = {
        "telegram_link": generate_telegram_link(token.token),
    }

    return render(
        request,
        "index.html",
        context=context,
    )

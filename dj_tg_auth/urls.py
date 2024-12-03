from django.contrib import admin
from django.urls import path

from authentication import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/telegram_login/", views.telegram_login),
    path("api/telegram_login/check/", views.telegram_login_check),
    path("", views.index),
]

# backend/users/urls.py
from django.urls import path
from .views import SetEmailWithPasswordView

urlpatterns = [
    path("set_email/", SetEmailWithPasswordView.as_view(), name="set-email-with-password"),
]
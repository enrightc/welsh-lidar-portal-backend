from __future__ import annotations

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if password is None:
            return None

        login = username or kwargs.get(User.USERNAME_FIELD) or kwargs.get("email")
        if not login:
            return None

        q = Q(**{f"{User.USERNAME_FIELD}__iexact": login})

        # Also allow email login if the model has an email field and it's not already USERNAME_FIELD
        try:
            User._meta.get_field("email")
            if User.USERNAME_FIELD != "email":
                q |= Q(email__iexact=login)
        except Exception:
            pass

        user = User.objects.filter(q).first()
        if not user:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
from django.shortcuts import render

# backend/users/views.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class SetEmailWithPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get("email", "").strip()
        current_password = request.data.get("current_password", "")

        if not email:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        if not current_password:
            return Response(
                {"current_password": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        # Check password is correct
        if not user.check_password(current_password):
            return Response(
                {"current_password": ["Incorrect password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Optional: prevent duplicates (helps give a friendly error)
        if User.objects.filter(email__iexact=email).exclude(pk=user.pk).exists():
            return Response(
                {"email": ["This email is already in use."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.email = email
        user.save(update_fields=["email"])

        # Keep response simple (you can return more fields if you want)
        return Response(
            {"id": user.id, "username": user.username, "email": user.email},
            status=status.HTTP_200_OK,
        )

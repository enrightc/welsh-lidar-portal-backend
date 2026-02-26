"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.api import views as users_api_views
from django.views.generic import RedirectView

# Serving files uploaded by a user during development
from django.conf import settings
from django.conf.urls.static import static
import os

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/profiles/', users_api_views.ProfileList.as_view()),
    path('api/profiles/<int:pk>/', users_api_views.ProfileDetail.as_view()),
    path('api/profiles/<int:pk>/update/', users_api_views.ProfileUpdate.as_view()),
    path('api/profiles/username/<str:username>/', users_api_views.ProfileByUsername.as_view()),
    path("api/", include("records.api.urls")),
    path('api/news/', include('news.urls')), 
    # Djoser provides ready-made endpoints for user authentication (register, login, logout, etc.)
    # The frontend (e.g. React) will send requests here during authentication — users won't see or visit these URLs directly.
    path('api-auth-djoser/', include('djoser.urls')),
    path('api-auth-djoser/', include('djoser.urls.authtoken')),
    path("api/users/", include("users.urls")),
    path(
        'reset-password/<str:uid>/<str:token>',
        RedirectView.as_view(
            url=f'{FRONTEND_URL}/reset-password/%(uid)s/%(token)s',
            permanent=False,
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
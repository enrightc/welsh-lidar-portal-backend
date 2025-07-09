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
from records.api import views as records_api_views
from users.api import views as users_api_views

# Serving files uploaded by a user during development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/profiles/', users_api_views.ProfileList.as_view()),
    path('api/profiles/<int:pk>/', users_api_views.ProfileDetail.as_view()),
    path('api/records/', records_api_views.RecordList.as_view()),
    path('api/records/create/', records_api_views.RecordCreate.as_view()),
    # Djoser provides ready-made endpoints for user authentication (register, login, logout, etc.)
    # The frontend (e.g. React) will send requests here during authentication — users won't see or visit these URLs directly.
    path('api-auth-djoser/', include('djoser.urls')),
    path('api-auth-djoser/', include('djoser.urls.authtoken')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

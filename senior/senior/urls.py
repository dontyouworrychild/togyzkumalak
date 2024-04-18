"""
URL configuration for senior project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from togyzkumalak.views import register, get_my_data
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from togyzkumalak.views import GameHistory, GameSession

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify-token"),
    path('register/', register, name='register'),
    path('my_data/', get_my_data, name='get_my_data'),
    path('games/', include("togyzkumalak.urls")),
    path('users/', include("users.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

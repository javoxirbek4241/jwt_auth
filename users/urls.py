from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from django.urls import path
from .views import *
urlpatterns = [
    path('regis/', RegisterApi.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token_refresh/', TokenRefreshView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
]
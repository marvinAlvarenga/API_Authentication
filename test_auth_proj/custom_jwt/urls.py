from django.urls import path

from .views import LogOutAPIView, TokenRefreshAPIView


urlpatterns = [
    path('token/logout/', LogOutAPIView.as_view(), name='token-logout'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token-refresh'),
]
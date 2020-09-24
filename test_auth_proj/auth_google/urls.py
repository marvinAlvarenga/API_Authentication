from django.urls import path

from .views import AuthAPIView

urlpatterns = [
    path('token/', AuthAPIView.as_view(), name='social-login'),
]

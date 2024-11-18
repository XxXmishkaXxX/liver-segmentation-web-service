from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *


urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resend-code/', ResendCodeView.as_view(), name='resend_code'),
]

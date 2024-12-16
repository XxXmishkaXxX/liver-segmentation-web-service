from django.urls import path
from .views import *


urlpatterns = [
    path('data/', UserDataView.as_view(), name='user-data'),
    path('registration/', RegisterView.as_view()),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('resend-code/', ResendCodeView.as_view(), name='resend_code'),
]

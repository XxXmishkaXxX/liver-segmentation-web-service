from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, ConfirmEmailSerializer, ResendCodeSerializer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed


class MyTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            refresh = response.data.get("refresh")
            if refresh:
                # Устанавливаем refresh token в HttpOnly куку
                response.set_cookie(
                    key="refresh_token",
                    value=refresh,
                    httponly=True,
                    secure=False,  # Работает только с HTTPS
                    samesite="Strict",  # Защищает от CSRF
                    max_age=365 * 24 * 60 * 60,  # Истекает через 365 дней
                )
        return super().finalize_response(request, response, *args, **kwargs)


class RefreshTokenView(APIView):
    def post(self, request):
        # Получаем refresh токен из куки
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            raise AuthenticationFailed('Refresh token not provided in cookies')
        
        try:
            # Декодируем refresh токен
            refresh = RefreshToken(refresh_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid refresh token')

        # Создаем новый access токен
        access_token = refresh.access_token

        # Возвращаем новый access токен
        return Response({
            'access_token': str(access_token)
        })



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        user.email_confirmation_code.send_email()
        return Response({"detail": "User registered. Check your email for confirmation code."}, status=status.HTTP_201_CREATED)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email confirmed. You can now log in."}, status=status.HTTP_200_OK)

class ResendCodeView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = ResendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Код подтверждения отправлен на указанный email."}, status=status.HTTP_200_OK)



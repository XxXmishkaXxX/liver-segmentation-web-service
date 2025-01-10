from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (RegisterSerializer, 
                          ConfirmEmailSerializer, 
                          ResendCodeSerializer, 
                          UserSerializer,
                          ChangePasswordSerializer,)
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta


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
                    samesite='Lax',
                    max_age=timedelta(days=365)
                )
        return super().finalize_response(request, response, *args, **kwargs)


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            raise AuthenticationFailed('Refresh token not provided')

        try:
            # Декодируем refresh токен
            refresh = RefreshToken(refresh_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid refresh token')

        # Создаем новый access токен
        access_token = refresh.access_token

        # Возвращаем новый access токен
        return Response({
            'access': str(access_token)
        })



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        user.email_confirmation_code.send_email()
        return Response({"success": '''Пользователь зарегистрирован. 
                        Проверьте свою электронную почту на наличие кода подтверждения.'''},
                        status=status.HTTP_201_CREATED)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": '''Электронное письмо подтверждено.
                        Теперь вы можете войти в систему.'''},
                        status=status.HTTP_200_OK)

class ResendCodeView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = ResendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Код подтверждения отправлен на указанный email."}, status=status.HTTP_200_OK)


class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user)
        print(user.data)
        return Response(user.data)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пароль успешно изменён."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
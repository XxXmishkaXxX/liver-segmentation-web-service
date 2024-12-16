from rest_framework import serializers
from .models import User, EmailConfirmationCode
from string import digits, punctuation
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    domains = ['mail.ru', 'gmail.com', 'yandex.ru']

    def validate_first_name(self, value: str) -> str:
        if len(value) > 255 or len(value) < 2:
            raise serializers.ValidationError('Имя должно быть длинной от 2 до 255 символов')
        if any(char in digits + punctuation for char in value):
            raise serializers.ValidationError('Имя не должно содержать цифры и спецсимволы')
        return value.capitalize()

    def validate_last_name(self, value: str) -> str:
        if len(value) > 255 or len(value) < 2:
            raise serializers.ValidationError('Фамилия должна быть длинной от 2 до 255 символов')
        if any(char in digits + punctuation for char in value):
            raise serializers.ValidationError('Фамилия не должна содержать цифры и спецсимволы')
        return value.capitalize()

    def validate_email(self, email):
        if email.split('@')[1] not in self.domains:
            raise serializers.ValidationError("Вы использовали не разрешенный почтовый домен.")
        return email

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        EmailConfirmationCode.objects.create(user=user)
        return user


class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        try:
            user = User.objects.get(email=email)
            confirmation = EmailConfirmationCode.objects.get(user=user, code=code)
        except (User.DoesNotExist, EmailConfirmationCode.DoesNotExist):
            raise serializers.ValidationError("Invalid email or confirmation code.")
        if not confirmation.is_valid():
            raise serializers.ValidationError("Confirmation code expired.")
        return attrs

    def save(self, **kwargs):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        EmailConfirmationCode.objects.filter(user=user).delete()
        return user


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        if user.is_active:
            raise serializers.ValidationError("Email уже подтвержден.")
        return email

    def save(self, **kwargs):
        email = self.validated_data["email"]
        user =  User.objects.get(email=email)
        confirmation, created = EmailConfirmationCode.objects.get_or_create(user=user)
        if not created:  # Если запись уже существует, обновляем код
            confirmation.regenerate_code()
        confirmation.send_email()
        return user
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
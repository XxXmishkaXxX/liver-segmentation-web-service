from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
import random
import string
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        print(email, password,)
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



def generate_code(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class EmailConfirmationCode(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="email_confirmation_code"
    )
    code = models.CharField(max_length=6, default=generate_code, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self) -> bool:
        return now() - self.created_at <= timedelta(minutes=5)

    def regenerate_code(self):
        self.code = generate_code()
        self.created_at = now()
        self.save()

    def send_email(self):
        subject = "Подтверждение электронной почты"
        context = {
            "code": self.code,
            "user": self.user,
        }
        text_message = f"Ваш код подтверждения: {self.code}"
        html_message = render_to_string("email_confirmation.html", context)
        recipient_list = [self.user.email]
        
        email = EmailMultiAlternatives(
            subject, text_message, settings.EMAIL_HOST_USER, recipient_list
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
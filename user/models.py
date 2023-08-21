from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission, Group)
from django.db import models
from django.db import transaction
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Необходимо указать username')
        try:
            with transaction.atomic():
                user = self.model(username=username, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_groups'  # Добавить это поле
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Разрешения пользователя',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_permissions'  # Добавить это поле
    )
    username = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=40, unique=True, blank=True, null=True, verbose_name='email')
    password = models.CharField(max_length=128, blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    authorization_code = models.CharField(max_length=500, blank=True, null=True, verbose_name='authorization_code_for_api')
    access_token = models.CharField(max_length=500, blank=True, null=True, verbose_name='access_token_for_api')
    refresh_token = models.CharField(max_length=500, blank=True, null=True, verbose_name='refresh_token_for_api')
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f'{self.email}, {self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

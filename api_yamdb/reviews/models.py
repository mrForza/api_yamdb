from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'админ'),
)


class User(AbstractUser):
    role = models.CharField(
        max_length=256,
        verbose_name='Роль',
        default='user',
        choices=ROLES,
    )
    bio = models.TextField(
        max_length=256,
        verbose_name='Биография',
        blank=True
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email address',
        unique=True,
        blank=False,
    )
    confirmation_code = models.CharField(
        max_length=6,
        verbose_name='Код подтверждения',
        blank=True,
    )
    password = models.CharField(_('password'), max_length=128, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        default_related_name = 'users'

    def __str__(self):
        return self.username

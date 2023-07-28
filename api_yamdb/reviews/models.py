from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core import validators


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



class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Категория')
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='Слаг',
                            validators=[validators.validate_slug])
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField( max_length=256,
                            verbose_name='Жанр произведения'
    )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='Слаг',
                            validators=[validators.validate_slug])
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField( verbose_name='Год выпуска')
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(Genre,
                                   through='TitleGenre',
                                   related_name='titles',
                                   verbose_name='Жанр произведения')
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='Категория произведения')
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title,
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE,
                              related_name='titles',
                              verbose_name='Произведение',)
    genre = models.ForeignKey(Genre,
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='genres',
                              verbose_name='Жанр',)

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

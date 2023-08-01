from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.validators import validate_year

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


class BaseModel(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
        validators=[validators.validate_slug]
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('name',)


class Category(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Произведение'
    )
    year = models.IntegerField(verbose_name='Год выпуска',
                               db_index=True,
                               validators=[validate_year])
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.SmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        unique_together = ('author', 'title')


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        unique_together = ('review', 'author')

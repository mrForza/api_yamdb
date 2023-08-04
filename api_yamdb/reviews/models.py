from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.validators import (
    username_validator, validate_year
)


MAX_LENGTH_SLUG = 50
MAX_LENGTH_NAME = 150
MAX_LENGTH_CODE = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_BASE_TITLE = 256

ROLE_USER = 'user'
ROLE_MODER = 'moderator'
ROLE_ADMIN = 'admin'

ROLES = (
    (ROLE_USER, 'пользователь'),
    (ROLE_MODER, 'модератор'),
    (ROLE_ADMIN, 'админ'),
)

SCORE_VALIDATION_ERROR = 'Оценка должна быть в диапазоне от 1 до 10'


class User(AbstractUser):

    username = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Имя пользователя',
        unique=True,
        validators=(username_validator, ),
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Фамилия',
        blank=True,
    )
    role = models.CharField(
        max_length=len(max([role[0] for role in ROLES], key=len)),
        verbose_name='Роль',
        default=ROLE_USER,
        choices=ROLES,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        verbose_name='email address',
        unique=True,
    )
    confirmation_code = models.CharField(
        max_length=MAX_LENGTH_CODE,
        verbose_name='Код подтверждения',
        blank=True,
    )
    password = models.CharField(
        _('password'),
        max_length=MAX_LENGTH_CODE,
        blank=True,
    )
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        default_related_name = 'users'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @property
    def is_moder(self):
        return self.role == ROLE_MODER


class BaseModel(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_BASE_TITLE,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG,
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
        max_length=MAX_LENGTH_BASE_TITLE,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        db_index=True,
        validators=[validate_year]
    )
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
        ordering = ('name', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class ReviewCommentMixin(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('pub_date', )


class Review(ReviewCommentMixin):
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, SCORE_VALIDATION_ERROR),
            MaxValueValidator(10, SCORE_VALIDATION_ERROR)
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            ),
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:50]


class Comment(ReviewCommentMixin):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'review'),
                name='unique_author_review'
            ),
        )
        verbose_name = 'Комментарий'
        verbose_name = 'Комментарии'

    def __str__(self):
        return self.text[:50]

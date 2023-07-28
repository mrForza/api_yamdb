from django.db import models
from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


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
        User, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='reviews',
        unique=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='comments',
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
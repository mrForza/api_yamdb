from django.db import models
from django.core import validators

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
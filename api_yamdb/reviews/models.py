from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Категория')
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='Слаг')
    
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
                            verbose_name='Слаг')
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return self.name
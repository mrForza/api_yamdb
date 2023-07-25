from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='Слаг')
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

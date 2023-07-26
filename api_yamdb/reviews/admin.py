from django.contrib import admin
from reviews.models import Category, Genre

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = 'не задано'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = 'не задано'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
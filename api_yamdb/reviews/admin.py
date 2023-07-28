from django.contrib import admin
from reviews.models import (
    Review, Comment, Genre, Category, Title
)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'score'
    )
    search_fields = ('text', )
    empty_value_display = 'не задано'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text'
    )
    search_fields = ('text', )
    empty_value_display = 'не задано'


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


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'year',
                    'description',
                    'category',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = 'не задано'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.register(Review, ReviewAdmin)
admin.register(Comment, CommentAdmin)

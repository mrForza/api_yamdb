from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reviews.models import Category, Comment, Genre, Review, Title, User


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score')
    search_fields = ('text', )
    empty_value_display = 'не задано'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')
    search_fields = ('text', )
    empty_value_display = 'не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = 'не задано'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = 'не задано'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = 'не задано'


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('role', 'bio', )}),
)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.register(Review, ReviewAdmin)
admin.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)

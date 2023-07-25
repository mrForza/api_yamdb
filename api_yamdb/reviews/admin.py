from django.contrib import admin
from reviews.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = 'не задано'


admin.site.register(Category, CategoryAdmin)
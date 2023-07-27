from django.contrib import admin
from reviews.models import Review, Comment


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


admin.register(Review, ReviewAdmin)
admin.register(Comment, CommentAdmin)

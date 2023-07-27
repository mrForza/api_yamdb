from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import User


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('role', 'bio', )}),
)

admin.site.register(User, UserAdmin)

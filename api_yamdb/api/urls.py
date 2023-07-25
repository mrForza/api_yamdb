from api.views import (CategoryViewSet)
from django.urls import include, path

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
]

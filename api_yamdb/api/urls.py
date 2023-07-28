from rest_framework.routers import DefaultRouter
from api.views import (
    CommentViewSet, ReviewViewSet, CategoryViewSet,
    GenreViewSet, TitleViewSet
)
from django.urls import path, include


router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet, basename='comments'
)



urlpatterns = [
    path('v1/', include(router.urls))
]
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (APISign, CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, TokenView,
                       UserViewSet)

router = DefaultRouter()

router.register('users', UserViewSet)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet, basename='comments'
)

auth = [
    path('token/', TokenView.as_view(), name='token'),
    path('signup/', APISign.as_view(), name='signup'),
]

urlpatterns = [
    path('v1/auth/', include(auth)),
    path('v1/', include(router.urls)),
]

from api.views import (APISign, CategoryViewSet, CommentViewSet, GenreViewSet,
                       MeDetail, ReviewViewSet, TitleViewSet, TokenView,
                       UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

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


urlpatterns = [
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/auth/signup/', APISign.as_view(), name='signup'),
    path('v1/users/me/', MeDetail.as_view(), name='me_detail'),
    path('v1/', include(router.urls)),
]

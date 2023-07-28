from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, MeDetail, APISign, TokenView, CategoryViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/auth/signup/', APISign.as_view(), name='signup'),
    path('v1/users/me/', MeDetail.as_view(), name='me_detail'),
    path('v1/', include(router.urls)),


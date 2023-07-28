from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, MeDetail, APISign, TokenView


router = DefaultRouter()
router.register('v1/users', UserViewSet)


urlpatterns = [
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/auth/signup/', APISign.as_view(), name='signup'),
    path('v1/users/me/', MeDetail.as_view(), name='me_detail'),
    path('', include(router.urls)),
]

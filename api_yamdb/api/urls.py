from rest_framework.routers import DefaultRouter
from api.views import CommentViewSet, ReviewViewSet
from django.urls import path, include


router = DefaultRouter()

# Если модель Title будет сделана, нужно поменять на r'titles/(?P<title_id>^[-a-zA-Z0-9_]+$)/reviews'
router.register(r'reviews', ReviewViewSet, basename='reviews')
# Если модель Title будет сделана, нужно поменять на r'titles/(?P<title_id>^[-a-zA-Z0-9_]+$)/reviews/(?P<review_id>[\d]+)/comment'
router.register(r'reviews/(?P<review_id>[\d]+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls))
]
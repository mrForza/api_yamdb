from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from django.core.exceptions import ObjectDoesNotExist


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        try:
            return get_object_or_404(
                Review,
                pk=self.kwargs.get('review_id')
            ).comments
        except ObjectDoesNotExist:
            return None


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        try:
            return get_object_or_404(
                Review,
                pk=self.kwargs.get('review_id')
            ).comments
        except ObjectDoesNotExist:
            return None
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

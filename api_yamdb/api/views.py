from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Review
from .serializers import ReviewSerializer, CommentSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters, mixins, viewsets

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleCreateSerializer)
from api.filters import TitleFilter
from reviews.models import Category, Genre, Title

from django_filters.rest_framework import DjangoFilterBackend


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        try:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return get_object_or_404(
                Title,
                pk=self.kwargs.get('title_id')
            ).reviews.all()
        except ObjectDoesNotExist:
            return None


    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        try:
            return get_object_or_404(
                Review,
                pk=self.kwargs.get('review_id')
            ).comments.all()
        except ObjectDoesNotExist:
            return None
        
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        )


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # написать пермишен
    # permission_classes = 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # написать пермишен
    # permission_classes = 
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all() # Можно здесь прописать функцию подсчета рейтинга. Нужна модель Review
    # написать пермишен
    # permission_classes =
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer
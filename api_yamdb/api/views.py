from rest_framework import filters, mixins, viewsets

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleCreateSerializer)
from api.filters import TitleFilter
from reviews.models import Category, Genre, Title

from django_filters.rest_framework import DjangoFilterBackend


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
    
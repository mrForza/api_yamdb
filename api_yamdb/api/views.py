from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action

from api.serializers import CategorySerializer
from reviews.models import Category


@action(detail=True, methods=['LIST', 'POST', 'DEL'])
class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # написать пермишен
    # permission_classes = 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
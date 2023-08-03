from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnlyForList,
                             IsAuthorOrAdminOrModerOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, MeUserSerializer,
                             ReviewSerializer, SignSerializer,
                             TitleCreateSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerOrReadOnly, )

    def get_title_object(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title_object().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title_object()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerOrReadOnly, )

    def get_review_object(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review_object().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review_object()
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
    permission_classes = (IsAdminOrReadOnlyForList, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnlyForList, )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnlyForList, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')


class MeDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = MeUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APISign(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            user = get_object_or_404(
                User,
                username=request.data.get('username'),
                email=request.data.get('email'),
            )
            send_mail(
                subject='Confirmation code',
                message=f'Ваш код подтверждения: {user.confirmation_code}',
                from_email='api_yamdb@yamdb.not',
                recipient_list=[user.email],
                fail_silently=True,
            )
            return Response(request.data, status=status.HTTP_200_OK)
        except Exception:
            serializer = SignSerializer(data=request.data)
            if serializer.is_valid():
                email = request.data.get('email')
                confirmation_code = str(randint(0, 999999)).zfill(6)
                send_mail(
                    subject='Confirmation code',
                    message=f'Ваш код подтверждения: {confirmation_code}',
                    from_email='api_yamdb@yamdb.not',
                    recipient_list=[email],
                    fail_silently=True,
                )
                serializer.save(confirmation_code=confirmation_code)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(TokenObtainPairView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid():
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = request.data.get('confirmation_code')
            if confirmation_code == user.confirmation_code:
                refresh = RefreshToken.for_user(user)
                data = {
                    'token': str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)
            error = {
                'confirmation_code':
                'Отсутсвует обязательное поле или оно не корректно',
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

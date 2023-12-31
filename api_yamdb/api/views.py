from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.filters import TitleFilter
from api.mixins import MyMixinSet
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsAuthorOrAdminOrModerOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, MeUserSerializer,
                             ReviewSerializer, SignSerializer,
                             TitleCreateSerializer, TitleReadOnlySerializer,
                             TokenSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


class CategoryViewSet(MyMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(MyMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleReadOnlySerializer


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
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review_object().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review_object()
        )


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdmin, )
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated, ),
    )
    def get_and_patch(self, request):
        if request.method == 'GET':
            return Response(
                MeUserSerializer(self.request.user).data,
                status=status.HTTP_200_OK
            )
        elif request.method == 'PATCH':
            serializer = MeUserSerializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class APISign(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, status_create = User.objects.get_or_create(
            username=request.data.get('username'),
            email=request.data.get('email'),
        )

        user.confirmation_code = str(default_token_generator.make_token(user))

        send_mail(
            subject='Confirmation code',
            message=f'Ваш код подтверждения: {user.confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(TokenObtainPairView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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

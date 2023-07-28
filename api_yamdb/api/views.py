from random import randint

from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from reviews.models import User
from api.serializers import (
    UserSerializer, SignSerializer, MeUserSerializer, TokenSerializer
)
from api.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin, )

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']


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
        elif User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ):
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

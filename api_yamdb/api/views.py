from random import randint

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from reviews.models import User
from api.serializers import UserSerializer, SignSerializer, MeUserSerializer
from api.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )


class MeDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        print(self.request.user)
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = MeUserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, username=self.request.user)
            serializer.save(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APISign(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            email = request.data.get('email')
            confirmation_code = str(randint(0, 999999)).zfill(6)
            send_mail(
                subject='Confirmation code',
                message=(f'Привет, {username}',
                         f'Ваш код подтверждения: {confirmation_code}'),
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
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = request.data.get('confirmation_code')
        if confirmation_code == user.confirmation_code:
            refresh = RefreshToken.for_user(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        error = {
            'confirmation_code':
            'Отсутсвует обязательное поле или оно не корректно',
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

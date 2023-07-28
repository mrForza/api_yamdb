from rest_framework import serializers, auth_users
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Title
from django.db.models import Avg
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class MeUserSerializer(UserSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        read_only_fields = ('role', )


class SignSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'confirmation_code',
        )
        model = User
        extra_kwargs = {'confirmation_code': {'write_only': True}}

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено')
        return data


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'confirmation_code',
        )
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ['id', 'name', 'year', 'rating',
                  'description', 'genre', 'category']
        model = Title
        read_only_fields = ['name', 'year', 'rating',
                            'description', 'genre', 'category']
    def get_rating(self, obj):
        pass


class TitleCreateSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(queryset=Category.objects.all(),
                                slug_field='slug')
    genre = SlugRelatedField(queryset=Genre.objects.all(),
                             slug_field='slug',
                             many=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'description',
                  'genre', 'category']

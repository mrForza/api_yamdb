from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User

from reviews.models import MAX_LENGTH_NAME, MAX_LENGTH_CODE, MAX_LENGTH_EMAIL
from api.validators import username_validator, username_not_me


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

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role', )


class SignSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(username_validator, username_not_me),
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
    )

    class Meta:
        fields = (
            'username',
            'email',
            'confirmation_code',
        )
        model = User
        extra_kwargs = {'confirmation_code': {'write_only': True}}

    def create(self, validated_data):
        user, status_create = User.objects.get_or_create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user.confirmation_code = str(default_token_generator.make_token(user))
        return user

    def validate(self, data):
        user = User.objects.filter(email=data.get('email'))
        if user:
            if user[0].username != data.get('username'):
                raise ValidationError(
                    detail=('Запрос содержит "email" ',
                            'зарегистрированного пользователя')
                )
        user = User.objects.filter(username=data.get('username'))
        if user:
            if user[0].email != data.get('email'):
                raise ValidationError(
                    detail=('Запрос содержит "username" ',
                            'зарегистрированного пользователя')
                )
        return data


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(username_validator, username_not_me),
    )
    confirmation_code = serializers.CharField(max_length=MAX_LENGTH_CODE)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug'
        )
        model = Genre


class TitleReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category', 'rating'
        )
        read_only_fields = (
            'name', 'year', 'rating',
            'description', 'genre', 'category', 'rating'
        )

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                title=self.context['view'].kwargs.get('title_id'),
                author=self.context['request'].user
            ).exists():
                raise ValidationError(
                    detail='Вы уже оставили отзыв на это произведение!',
                    code=400
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Comment.objects.filter(
                review=self.context['view'].kwargs.get('review_id'),
                author=self.context['request'].user
            ).exists():
                raise ValidationError(
                    detail='Вы уже оставили комментарий на этот отзыв!',
                    code=400
                )
        return data

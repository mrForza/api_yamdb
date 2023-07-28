from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import (
    Review, Comment, Category, Genre, Title
)


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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    
    class Meta:
        model = Comment,
        fields = '__all__'

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title

from django.db.models import Avg


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
        ...# Можно здесь прописать функцию подсчета рейтинга. Нужна модель Review
#оставлю это пока здесь https://question-it.com/questions/5840768/kak-rasschitat-srednee-znachenie-nekotorogo-polja-v-modeljah-django-i-otpravit-ego-v-api-otdyha


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

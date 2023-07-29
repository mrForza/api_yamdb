from rest_framework import serializers

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
    username = serializers.CharField(max_length=256)

    class Meta:
        fields = (
            'username',
            'confirmation_code',
        )
        model = User

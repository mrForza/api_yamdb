import datetime as dt
import re

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError('Год должен быть меньше или равен текущему')
    return value


def username_validator(value):
    if not re.search(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            r'Используйте только буквы, цифры и символы @/./+/-/_'
        )
    return value


def username_not_me(value):
    if value == 'me':
        raise ValidationError(
            'Использовать имя me в качестве username запрещено'
        )
    return value

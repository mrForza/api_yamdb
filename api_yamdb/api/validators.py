import datetime as dt
import re

from django.core.exceptions import ValidationError


FAILED_NAME = 'me'


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError('Год должен быть меньше или равен текущему')
    return value


def username_validator(value):
    if not re.search(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            r'Используйте только буквы, цифры и символы @/./+/-/_'
        )

    if value == FAILED_NAME:
        raise ValidationError(
            f'Использовать имя {FAILED_NAME} в качестве username запрещено'
        )
    return value

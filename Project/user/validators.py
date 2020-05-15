from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        print('api')
        raise ValidationError(f'{value}s is not an even number')

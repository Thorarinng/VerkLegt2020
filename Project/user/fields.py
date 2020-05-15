from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _



class TelephoneInput(TextInput):
    # switch input type to type tel so that the numeric keyboard shows on mobile devices
    input_type = 'tel'


class CreditCardField(forms.CharField):
    def __init__(self, placeholder=None, *args, **kwargs):
        super(CreditCardField, self).__init__(
            # override default widget
            widget=TelephoneInput(attrs={
                'placeholder': placeholder
            }), *args, **kwargs)

    default_error_messages = {
        'invalid': _(u'The credit card number is invalid'),
        'negative': _(u'Credit card number cant be negative'),
        'length': _(u'Must contain 16-digits'),
    }

    def clean(self, value):
        try:
            int(value)
        except:
            raise forms.ValidationError(
                'Card Number must be of a positive integer value')
        # ensure no spaces or dashes
        card = value.replace(' ', '').replace('-', '')
        if int(value) < 0:
            raise forms.ValidationError(self.error_messages['negative'])

        if not len(card) == 16:
            raise forms.ValidationError(self.error_messages['length'])

        return card


class CVCField(forms.CharField):
    def __init__(self, placeholder=None, *args, **kwargs):
        super(CVCField, self).__init__(
            # override default widget
            widget=TelephoneInput(attrs={
                'placeholder': placeholder
            }), *args, **kwargs)

    default_error_messages = {
        'invalid': _(u'The credit card number is invalid'),
        'letterPresent': _('Integers must be present INT/INT not aa/aa'),
    }

    def clean(self, value):
        try:
            date = value.replace('/', '')
            int(date)
        except:
            raise forms.ValidationError(self.error_messages['letterPresent'])
        return value


class CardExpirationField(forms.CharField):
    def __init__(self, placeholder=None, *args, **kwargs):
        super(CardExpirationField, self).__init__(
            # override default widget
            widget=TelephoneInput(attrs={
                'placeholder': placeholder
            }), *args, **kwargs)

    default_error_messages = {
        'invalid': _(u'The CARDEXPIRATION'),
        'invalidMonth': _(u'The month is invalid'),
        'invalidYear': _(u'The year is invalid'),
        'missing/': _('Missing /'),
        'letterPresent': _('Integers must be present INT/INT not aa/aa'),
    }

    def clean(self, value):

        try:
            val = value.split('/')
            print(val)
            month = val[0]
            year = val[1]
        except:
            raise forms.ValidationError(self.error_messages['missing/'])

        try:
            date = value.replace('/', '')
            int(date)
        except:
            raise forms.ValidationError(self.error_messages['letterPresent'])

        if not -1 < int(month) < 13:
            raise forms.ValidationError(self.error_messages['invalidMonth'])

        if int(year) < 20:
            print('missing')
            raise forms.ValidationError(self.error_messages['invalidYear'])

        if not len(value) == 5:
            raise forms.ValidationError(self.error_messages['invalid'])

        return value

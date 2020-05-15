from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

from user.models import User, ShippingAddress, PaymentMethod, SearchHistory
from .fields import CreditCardField, CVCField, CardExpirationField
from .validators import validate_even


# register
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Add a valid email address.')
    password1 = forms.PasswordInput(attrs={'class': 'option'})
    password2 = forms.PasswordInput(attrs={'class': 'option'})

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'firstName',
                  'lastName', 'phoneNumber', 'imgURL')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'option'}),
            'email': forms.TextInput(attrs={'class': 'option'}),
            'password1': forms.TextInput(attrs={'class': 'option'}),
            'password2': forms.PasswordInput(attrs={'class': 'option'}),
            'firstName': forms.TextInput(attrs={'class': 'option'}),
            'lastName': forms.TextInput(attrs={'class': 'option'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'option'}),
            'imgURL': forms.TextInput(attrs={'class': 'option'})
        }


# auth
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


# Edit Profile
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('imgURL', 'firstName', 'lastName', 'phoneNumber', 'password')
        # labels = {'password': 'New Password or enter your old one'}
        widgets = {
            'password': forms.PasswordInput()
        }


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ('pk',)
        fields = ('address1', 'address2', 'city',
                  'country', 'region', 'postalCode')


class PaymentMethodForm(forms.ModelForm):
    cardNumber = CreditCardField(
        placeholder='0000', min_length=16, max_length=16)
    cvc = CVCField(placeholder='123', max_length=3, min_length=3)
    cardExpiry = CardExpirationField(
        placeholder='MM/YY', max_length=5, min_length=5)

    class Meta:
        model = PaymentMethod
        fields = ('nameOnCard', 'cardNumber', 'cardExpiry', 'cvc')


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchHistory
        fields = ('string',)

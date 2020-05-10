from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

from user.models import User, ShippingAddress, PaymentMethod
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

# register
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    password1 = forms.PasswordInput(attrs={'class': 'form-control'})
    password2 = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'firstName', 'lastName', 'phoneNumber', 'imgURL')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'imgURL': forms.TextInput(attrs={'class': 'form-control'})
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
        fields = ('address1', 'address2', 'city', 'country', 'region', 'postalCode')


class PaymentMethodForm(forms.ModelForm):
    # MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    # baba = ['12']
    # YEARS = ['2020','2021']
    # expMonth = forms.ChoiceField(choices=MONTHS)
    # nameOnCard = forms.CharField(widget=forms.Select(choices=baba))
    # expYear = forms.ChoiceField(choices=MONTHS)



    class Meta:
        model = PaymentMethod
        fields = ('nameOnCard', 'cardNumber', 'cardExpiry', 'cvc')
        widgets = {
            'nameOnCard': forms.widgets.NumberInput(attrs={'placeholder': 'Name'}),
            'cardNumber': forms.widgets.NumberInput(attrs={'placeholder': '16-digits'}),
            'cardExpiry': forms.widgets.NumberInput(attrs={'placeholder': 'MM/YY'}),
            'cvc': forms.widgets.NumberInput(attrs={'placeholder': 'CVC'})
        }

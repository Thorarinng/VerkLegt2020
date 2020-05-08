from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

from user.models import User


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


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('imgURL', 'firstName', 'lastName', 'phoneNumber', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

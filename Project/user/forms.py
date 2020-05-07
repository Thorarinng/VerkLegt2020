from django.contrib.auth import authenticate
from django.forms import ModelForm, widgets, forms
from user.models import User
from django import forms


class ContactForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'name', 'last_login', 'active', 'employee', 'admin']

class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Go fuck yourself')

            if not user.check_password(password):
                raise forms.ValidationError('Incorrect PW')

        return super(UserLoginForm, self).clean(*args, **kwargs)

from django import forms

from core.utils.model_helper import get_field_attr
from .models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(validators=get_field_attr(User, 'username', 'validators', []),
                               max_length=get_field_attr(User, 'username', 'max_length'),
                               min_length=4)
    password = forms.CharField(validators=get_field_attr(User, 'password', 'validators', []))


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

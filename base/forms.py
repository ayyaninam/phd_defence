from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
from base.models import *


User = get_user_model()


class CustomPasswordValidator:
    def validate(self, password):
        # Check for minimum length
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Check for at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Check for at least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Check for at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

    def get_help_text(self):
        return "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character."


class LoginForm(forms.Form):

    email = forms.EmailField(
        label=_("Email"),
        validators=[validate_email],
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
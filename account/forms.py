from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'organization_name', 'first_name', 'last_name', 'phone_number', 'subdomain', 'password1', 'password2', 'role')

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Invalid email or password. Please try again.')

            # Validate the password using Django's built-in password validation
            try:
                validate_password(password, user=user)
            except ValidationError as error:
                raise forms.ValidationError(error.messages[0])
        return password
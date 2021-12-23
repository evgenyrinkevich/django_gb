import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
import django.forms as forms
from django.core.exceptions import ValidationError

from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'age', 'avatar'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise ValidationError('You are too young!')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not data.isascii():
            raise ValidationError('First name should be latin characters')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            'username', 'password', 'email', 'first_name', 'last_name', 'age', 'avatar'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            else:
                field.widget.attrs['class'] = f'form-control {field_name}'
                field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise ValidationError('You are too young!')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not data.isascii():
            raise ValidationError('First name should be latin characters')
        return data


class ShopUserChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            'old_password',
            'new_password1',
            'new_password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''

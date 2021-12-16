from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
import django.forms as forms
from django.core.exceptions import ValidationError

from authapp.models import ShopUser
from mainapp.models import ProductCategory


class AdminShopUserCreateForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'age', 'avatar', 'is_superuser'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise ValidationError('User is too young!')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not data.isascii():
            raise ValidationError('First name should be latin characters')
        return data


class AdminShopUserUpdateForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            'username', 'password', 'email', 'first_name', 'last_name', 'age', 'avatar', 'is_superuser', 'is_active')

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


class AdminProductCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from business.models import Business, BusinessArea
from users.models import User


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["user_email", "user_phone", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        return user


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ["user_email", 'first_name', "user_phone",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ['user_business_area',]

    def __init__(self, business_id, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        business = Business.objects.get(id=business_id)

        self.fields['user_business_area'].queryset = BusinessArea.objects.filter(business=business)

        self.fields['password'].widget = forms.HiddenInput()

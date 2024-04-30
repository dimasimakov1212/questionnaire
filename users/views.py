from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from users.forms import UserLoginForm, UserRegisterForm, UserForm, UserUpdateForm
from users.models import User


class UserLoginView(LoginView):
    """ Авторизация пользователя """

    model = User

    template_name = 'users/login.html'

    form_class = UserLoginForm


class UserRegisterView(CreateView):
    """ Регистрация пользователя """

    model = User

    form_class = UserRegisterForm

    template_name = 'users/register.html'

    success_url = reverse_lazy('users:login')


class UserProfileView(UpdateView):
    """ Изменение профиля пользователя """

    model = User

    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.kwargs['pk']})


class UserDetailView(DetailView):
    """ Информация о пользователе """

    model = User

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    """ Обновление объекта сферы деятельности пользователя """

    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None):

        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['business_id'] = self.kwargs.get('business_id')

        return kwargs

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.request.user.id})

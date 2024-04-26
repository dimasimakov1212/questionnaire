from django.contrib.auth.models import AbstractUser
from django.db import models

from business.models import BusinessArea


class User(AbstractUser):
    """ Модель пользователя """

    username = None

    user_email = models.EmailField(verbose_name='Почта', unique=True)
    user_phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    user_business_area = models.ForeignKey(BusinessArea, on_delete=models.CASCADE,
                                           verbose_name='Сфера деятельности', null=True, blank=True)
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

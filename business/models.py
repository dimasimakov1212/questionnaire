from django.db import models


class Business(models.Model):
    """ Модель типа бизнеса """

    business_title = models.CharField(max_length=150, verbose_name='Тип бизнеса')
    business_description = models.TextField(max_length=200, verbose_name='Описание бизнеса', null=True, blank=True)

    def __str__(self):
        return self.business_title

    class Meta:
        verbose_name = 'Бизнес'
        verbose_name_plural = 'Бизнесы'


class BusinessArea(models.Model):
    """ Модель сфера деятельности """

    business_area_title = models.CharField(max_length=100, verbose_name='Сфера деятельности')
    business_area_description = models.TextField(max_length=200, verbose_name='Описание сферы деятельности',
                                                 null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name='Тип бизнеса')

    def __str__(self):
        return f'{self.business_area_title}'

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = 'Сферы деятельности'

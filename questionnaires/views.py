from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from questionnaires.forms import UserBusinessForm
from users.models import User


class HomePageView(TemplateView):
    """ Главная страница """

    template_name = 'questionnaires/home.html'


def get_user_business(request):
    """ Получение объекта бизнес """

    form = UserBusinessForm(request.POST)  # класс-метод формы создания объекта
    data = {'form': form}  # контекстная информация

    # получаем данные формы
    if request.method == 'POST':

        if form.is_valid():

            business_area = form.save(commit=False)  # получаем данные из формы

            business = business_area.business  # получаем объект тип бизнеса

            business_id = business.id  # получаем ID объекта тип бизнеса

            # перенаправляем на форму получения сферы деятельности
            return redirect('users:user_update', business_id)

    return render(request, 'questionnaires/userbusiness_form.html', context=data)

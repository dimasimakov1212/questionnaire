from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView

from questionnaires.forms import UserBusinessForm, QuestionnaireForm
from questionnaires.models import Questionnaire
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


class QuestionnaireList(ListView):
    """ Список объектов опрос """

    model = Questionnaire
    template_name = 'questionnaires/questionnaires_list.html'
    context_object_name = 'questionnaires'


class QuestionnaireCreate(CreateView):
    """ Создание объекта опрос """

    model = Questionnaire
    form_class = QuestionnaireForm
    template_name = 'questionnaires/questionnaire_form.html'

    def form_valid(self, form):
        """ Проверка и сохранение данных """

        self.object = form.save(commit=False)
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('questionnaires:questionnaires_list')


class QuestionnaireUpdate(UpdateView):
    """ Изменение объекта опрос """

    model = Questionnaire
    form_class = QuestionnaireForm
    success_url = reverse_lazy('questionnaires:questionnaires_list')

    def form_valid(self, form):
        """ Проверка и сохранение данных """

        if form.is_valid():
            new_questionnaire = form.save()
            new_questionnaire.save()

        return super().form_valid(form)


class QuestionnaireDelete(DeleteView):
    """ Удаление объекта опрос """

    model = Questionnaire
    success_url = reverse_lazy('questionnaires:questionnaires_list')

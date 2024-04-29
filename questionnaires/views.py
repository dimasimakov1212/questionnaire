from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView, DetailView

from questionnaires.forms import UserBusinessForm, QuestionnaireForm, QuestionForm, AnswerForm
from questionnaires.models import Questionnaire, Question, Answer
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

    def get_queryset(self, *args, **kwargs):
        """ Определяем порядок вывода объектов """

        queryset = super().get_queryset(*args, **kwargs)

        user = self.request.user  # получаем текущего пользователя

        # если пользователь не является сотрудником, выводим только опубликованные опросы
        if not user.is_staff:
            queryset = queryset.filter(is_public=True)

        return queryset


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


class QuestionnaireDetail(DetailView):
    """ Просмотр деталей опроса со списком вопросов """

    model = Questionnaire
    context_object_name = 'questionnaire'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = self.get_object()
        context['questions'] = Question.objects.filter(questionnaire=questionnaire)

        return context


class QuestionnaireDelete(DeleteView):
    """ Удаление объекта опрос """

    model = Questionnaire
    success_url = reverse_lazy('questionnaires:questionnaires_list')


def question_create(request, pk):
    """ Создание объекта вопрос """

    questionnaire = Questionnaire.objects.get(id=pk)  # получаем объект опрос

    form = QuestionForm(request.POST)  # класс-метод формы создания объекта
    data = {'form': form, 'questionnaire': questionnaire}  # контекстная информация

    # получаем данные формы
    if request.method == 'POST':

        if form.is_valid():
            question = form.save(commit=False)  # получаем данные из формы

            question.questionnaire = questionnaire  # присваиваем вопросу объект опрос

            question.save()  # сохраняем объект

            pk = questionnaire.id  # получаем id опроса

            # перенаправляем на форму опроса
            return redirect('questionnaires:questionnaire_detail', pk)

    return render(request, 'questionnaires/question_form.html', context=data)  # шаблон создания вопроса


class QuestionUpdate(UpdateView):
    """ Изменение объекта вопрос """

    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        """ Проверка и сохранение данных """

        if form.is_valid():
            new_question = form.save()
            new_question.save()

        return super().form_valid(form)

    def get_success_url(self):
        questionnaire = self.object.questionnaire
        return reverse_lazy('questionnaires:questionnaire_detail', kwargs={'pk': questionnaire.pk})


class QuestionDelete(DeleteView):
    """ Удаление объекта вопрос """

    model = Question

    def get_context_data(self, **kwargs):
        """ Определяем контекстную информацию """

        context = super().get_context_data(**kwargs)
        question = self.get_object()  # получаем текущий объект вопрос
        context['questionnaire'] = question.questionnaire  # объект опрос
        context['question'] = question  # объект вопрос

        return context

    def get_success_url(self):
        questionnaire = self.object.questionnaire
        return reverse_lazy('questionnaires:questionnaire_detail', kwargs={'pk': questionnaire.pk})


class QuestionDetail(DetailView):
    """ Просмотр деталей вопроса со списком ответов """

    model = Question
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['answers'] = Answer.objects.filter(question=question)

        return context


def answer_create(request, pk):
    """ Создание объекта ответ """

    question = Question.objects.get(id=pk)  # получаем объект вопрос

    form = AnswerForm(request.POST)  # класс-метод формы создания объекта
    data = {'form': form, 'questionnaire': question}  # контекстная информация

    # получаем данные формы
    if request.method == 'POST':

        if form.is_valid():
            answer = form.save(commit=False)  # получаем данные из формы

            answer.question = question  # присваиваем ответу объект вопрос

            answer.save()  # сохраняем объект

            pk = question.id  # получаем id вопроса

            # перенаправляем на форму вопроса
            return redirect('questionnaires:question_detail', pk)

    return render(request, 'questionnaires/answer_form.html', context=data)  # шаблон создания ответа


class AnswerUpdate(UpdateView):
    """ Изменение объекта ответ """

    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        """ Проверка и сохранение данных """

        if form.is_valid():
            new_answer = form.save()
            new_answer.save()

        return super().form_valid(form)

    def get_success_url(self):
        question = self.object.question
        return reverse_lazy('questionnaires:question_detail', kwargs={'pk': question.pk})


class AnswerDelete(DeleteView):
    """ Удаление объекта ответ """

    model = Answer

    def get_context_data(self, **kwargs):
        """ Определяем контекстную информацию """

        context = super().get_context_data(**kwargs)
        answer = self.get_object()  # получаем текущий объект ответ
        context['question'] = answer.question  # объект вопрос
        context['answer'] = answer  # объект ответ

        return context

    def get_success_url(self):
        question = self.object.question
        return reverse_lazy('questionnaires:question_detail', kwargs={'pk': question.pk})

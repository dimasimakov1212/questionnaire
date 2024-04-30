from random import sample

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView, DetailView

from questionnaires.forms import UserBusinessForm, QuestionnaireForm, QuestionForm, AnswerForm, UserAnswerForm
from questionnaires.models import Questionnaire, Question, Answer, UserAnswer


class HomePageView(TemplateView):
    """ Главная страница """

    template_name = 'questionnaires/home.html'

    def get_context_data(self, **kwargs):
        """ Определяем контекстную информацию """

        context = super().get_context_data(**kwargs)

        questionnaires = Questionnaire.objects.filter(is_public=True)  # Получаем все опубликованные опросы

        user = self.request.user  # получаем текущего пользователя

        user_questionnaires = []  # задаем список опросов, в которых участвовал пользователь

        try:
            user_answers = UserAnswer.objects.filter(user=user)  # Получаем все ответы пользователя в опросах

            # получаем список опросов, в которых участвовал пользователь
            user_questionnaires = [user_answer.questionnaire for user_answer in user_answers]

        except TypeError:
            pass

        # если опубликованные опросы есть, выводим случайный опрос на главную страницу
        if len(questionnaires) >= 1:
            questionnaire_random = sample(list(questionnaires), 1)[0]  # Получаем 1 случайный опрос

            context['questionnaire_random'] = questionnaire_random  # объект опрос

            # если пользователь уже участвовал в опросе, задаем метку
            if questionnaire_random in user_questionnaires:
                context['questionnaire_done'] = True

        return context


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
        answers = Answer.objects.filter(question=question)

        # next_questions = get_next_question(answers)
        # print(next_questions)

        context['answers'] = answers
        # context['next_questions'] = next_questions

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


def user_first_answer_create(request, pk):
    """ Создание объекта ответ пользователя """

    questionnaire = Questionnaire.objects.get(id=pk)  # получаем объект опрос

    # получаем первый вопрос
    question = Question.objects.get(questionnaire=questionnaire, is_first=True)

    form = UserAnswerForm(question, request.POST)  # класс-метод формы создания объекта
    data = {'form': form, 'question': question}  # контекстная информация

    # получаем данные формы
    if request.method == 'POST':

        if form.is_valid():
            user_answer = form.save(commit=False)  # получаем данные из формы

            user = request.user  # получаем текущего пользователя

            user_answer.user = user  # присваиваем ответу пользователя объект пользователь
            user_answer.question = question  # присваиваем ответу пользователя объект вопрос
            user_answer.questionnaire = questionnaire  # присваиваем ответу пользователя объект опрос

            user_answer.save()  # сохраняем объект

            try:
                # получаем ID следующего вопроса
                next_question_id = user_answer.answer.next_question.id

            except AttributeError:

                # если следующего вопроса нет, присваиваем None
                next_question_id = None

            # если есть следующий вопрос, переходим к нему
            if next_question_id:

                # перенаправляем на форму вопроса
                return redirect('questionnaires:user_next_answer_create', next_question_id)

            else:
                # если вопроса нет, перенаправляем на завершающую страницу
                return redirect('questionnaires:questionnaire_end')

    return render(request, 'questionnaires/useranswer_form.html', context=data)  # шаблон создания ответа


def user_next_answer_create(request, next_question_id):
    """ Создание объекта ответ пользователя """

    # получаем следующий вопрос
    question = Question.objects.get(id=next_question_id)

    questionnaire = question.questionnaire  # получаем объект опрос

    form = UserAnswerForm(question, request.POST)  # класс-метод формы создания объекта
    data = {'form': form, 'question': question}  # контекстная информация

    # получаем данные формы
    if request.method == 'POST':

        if form.is_valid():
            user_answer = form.save(commit=False)  # получаем данные из формы

            user = request.user  # получаем текущего пользователя

            user_answer.user = user  # присваиваем ответу пользователя объект пользователь
            user_answer.question = question  # присваиваем ответу пользователя объект вопрос
            user_answer.questionnaire = questionnaire  # присваиваем ответу пользователя объект опрос

            user_answer.save()  # сохраняем объект

            try:
                # получаем ID следующего вопроса
                next_question_id = user_answer.answer.next_question.id

            except AttributeError:

                # если следующего вопроса нет, присваиваем None
                next_question_id = None

            # если есть следующий вопрос, переходим к нему
            if next_question_id:

                # перенаправляем на форму вопроса
                return redirect('questionnaires:user_next_answer_create', next_question_id)

            else:
                # если вопроса нет, перенаправляем на завершающую страницу
                return redirect('questionnaires:questionnaire_end')

    return render(request, 'questionnaires/useranswer_form.html', context=data)  # шаблон создания ответа


def questionnaire_end_view(request):
    """ Сообщение о завершении опроса """

    return render(request, 'questionnaires/questionnaire_end.html')

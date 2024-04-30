from django.db import models

from users.models import User


class Questionnaire(models.Model):
    """ Модель объекта опрос """

    questionnaire_title = models.CharField(max_length=100, verbose_name='Опрос')
    questionnaire_text = models.TextField(verbose_name='Описание опроса', null=True, blank=True)
    is_public = models.BooleanField(default=False, verbose_name='Опубликован')

    def __str__(self):
        return self.questionnaire_title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    """ Модель объекта вопрос """

    question_title = models.CharField(max_length=100, verbose_name='Вопрос')
    question_text = models.TextField(verbose_name='Описание вопроса', null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE,
                                      verbose_name='Опрос', null=True, blank=True)
    is_first = models.BooleanField(default=False, verbose_name='Начальный вопрос')

    def __str__(self):
        return self.question_title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    """ Модель объекта ответ """

    answer = models.CharField(max_length=150, verbose_name='Ответ')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос',
                                 related_name='first_question', null=True, blank=True)
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Следующий вопрос',
                                      related_name='next_question', null=True, blank=True)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class UserAnswer(models.Model):
    """ Модель объекта ответы пользователя """

    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Выберите ответ', null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE,
                                      verbose_name='Опрос', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.question} - {self.answer}'

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'

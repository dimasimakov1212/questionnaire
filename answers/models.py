from django.db import models

from questionnaires.models import Question, Answer, Questionnaire
from users.models import User


class Action(models.Model):
    """ Модель объекта действие """

    action_question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                        verbose_name='Вопрос', null=True, blank=True)
    action_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ', null=True, blank=True)
    action_next_question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                             verbose_name='Следующий вопрос', null=True, blank=True)

    def __str__(self):
        return f'{self.action_question} - {self.action_answer}'

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'


class UserAnswer(models.Model):
    """ Модель объекта ответы пользователя """

    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ', null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE,
                                      verbose_name='Опрос', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.question}'

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'

from django.contrib import admin

from questionnaires.models import Questionnaire, Question, Answer


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('questionnaire_title', 'is_public')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'is_first')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'next_question')

from django import forms

from business.models import BusinessArea
from questionnaires.models import Questionnaire, Question, Answer


class UserBusinessForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(UserBusinessForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BusinessArea
        fields = ('business',)


class QuestionnaireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(QuestionnaireForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Questionnaire
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(QuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        exclude = ('questionnaire',)


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(AnswerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ('answer',)

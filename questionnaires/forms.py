from django import forms

from business.models import BusinessArea
from questionnaires.models import Questionnaire, Question, Answer, UserAnswer


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

        fields = ('question_title', 'question_text',)


class FirstQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(FirstQuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ('question_title', 'question_text', 'is_first')


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(AnswerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ('answer', 'next_question')


class UserAnswerForm(forms.ModelForm):
    def __init__(self, question, *args, **kwargs):

        super(UserAnswerForm, self).__init__(*args, **kwargs)

        # в поле answer выводим только объекты с вязанные с текущим вопросом
        self.fields['answer'].queryset = Answer.objects.filter(question=question)

    class Meta:
        model = UserAnswer
        fields = ('answer',)

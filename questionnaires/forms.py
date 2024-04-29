from django import forms

from business.models import BusinessArea
from questionnaires.models import Questionnaire


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
        fields = ('questionnaire_title', 'questionnaire_text')

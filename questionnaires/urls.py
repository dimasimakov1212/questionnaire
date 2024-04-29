from django.urls import path

from questionnaires.apps import QuestionnairesConfig
from questionnaires.views import HomePageView, get_user_business, QuestionnaireList, QuestionnaireCreate, \
    QuestionnaireUpdate, QuestionnaireDelete

app_name = QuestionnairesConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('user_business/', get_user_business, name='user_business'),
    path('questionnaires_list/', QuestionnaireList.as_view(), name='questionnaires_list'),
    path('questionnaire_create/', QuestionnaireCreate.as_view(), name='questionnaire_create'),
    path('questionnaire_update/<int:pk>/', QuestionnaireUpdate.as_view(), name='questionnaire_update'),
    path('questionnaire_delete/<int:pk>/', QuestionnaireDelete.as_view(), name='questionnaire_delete'),
    ]

from django.urls import path

from questionnaires.apps import QuestionnairesConfig
from questionnaires.views import HomePageView, get_user_business, QuestionnaireList, QuestionnaireCreate, \
    QuestionnaireUpdate, QuestionnaireDelete, QuestionnaireDetail, question_create, QuestionUpdate, QuestionDelete, \
    QuestionDetail

app_name = QuestionnairesConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('user_business/', get_user_business, name='user_business'),
    path('questionnaires_list/', QuestionnaireList.as_view(), name='questionnaires_list'),
    path('questionnaire_create/', QuestionnaireCreate.as_view(), name='questionnaire_create'),
    path('questionnaire_update/<int:pk>/', QuestionnaireUpdate.as_view(), name='questionnaire_update'),
    path('questionnaire_delete/<int:pk>/', QuestionnaireDelete.as_view(), name='questionnaire_delete'),
    path('questionnaire_detail/<int:pk>/', QuestionnaireDetail.as_view(), name='questionnaire_detail'),
    path('question_create/<int:pk>/', question_create, name='question_create'),
    path('question_update/<int:pk>/', QuestionUpdate.as_view(), name='question_update'),
    path('question_delete/<int:pk>/', QuestionDelete.as_view(), name='question_delete'),
    path('question_detail/<int:pk>/', QuestionDetail.as_view(), name='question_detail'),
    ]

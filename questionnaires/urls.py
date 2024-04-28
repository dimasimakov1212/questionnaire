from django.urls import path

from questionnaires.apps import QuestionnairesConfig
from questionnaires.views import HomePageView, get_user_business

app_name = QuestionnairesConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('user_business/', get_user_business, name='user_business'),
    ]

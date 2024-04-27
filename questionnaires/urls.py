from django.urls import path

from questionnaires.apps import QuestionnairesConfig
from questionnaires.views import HomePageView

app_name = QuestionnairesConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    ]

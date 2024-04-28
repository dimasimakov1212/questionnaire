from django.contrib.auth.views import LogoutView
from django.urls import path


from business.apps import BusinessConfig
from business.views import BusinessList, BusinessCreate, BusinessDetail, BusinessUpdate, BusinessDeleteView, \
    business_area_create, BusinessAreaUpdate, BusinessAreaDelete

app_name = BusinessConfig.name

urlpatterns = [
    path('businesses/', BusinessList.as_view(), name='business_list'),
    path('business_create/', BusinessCreate.as_view(), name='business_create'),
    path('business_detail/<int:pk>/', BusinessDetail.as_view(), name='business_detail'),
    path('business_update/<int:pk>/', BusinessUpdate.as_view(), name='business_update'),
    path('business_delete/<int:pk>/', BusinessDeleteView.as_view(), name='business_delete'),
    path('business_area_create/<int:pk>/', business_area_create, name='business_area_create'),
    path('business_area_update/<int:pk>/', BusinessAreaUpdate.as_view(), name='business_area_update'),
    path('business_area_delete/<int:pk>/', BusinessAreaDelete.as_view(), name='business_area_delete'),
    ]

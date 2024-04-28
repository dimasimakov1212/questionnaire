from django.contrib.auth.views import LogoutView
from django.urls import path


from users.apps import UsersConfig
from users.views import UserRegisterView, UserLoginView, UserProfileView, UserDetailView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('user_profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    # path('user_update/<int:user_id>,<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user_update/<int:business_id>/', UserUpdateView.as_view(), name='user_update'),
    ]

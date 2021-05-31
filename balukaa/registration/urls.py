import debug_toolbar
from django.urls import path
from .views import UserCreateView, UserLoginView, UserLogoutView

app_name = 'registration'
urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]

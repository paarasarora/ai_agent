from django.urls import path
from .views import *
app_name = 'users'

urlpatterns = [
    path('create-users/',create_user, name='create_user'),
    path('my-account/', my_account, name='my_account'),
    path('login/', Login.as_view(), name='user_login'),
    path('login-test/', debug_login, name='login_test'),
]

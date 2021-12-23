
from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.LogoutView.as_view(), name='logout'),
    path('register/', authapp.register, name='register'),
    path('verify/<str:email>/<str:activation_key>/', authapp.verify, name='verify'),
    path('edit/', authapp.edit, name='edit'),
    path('change_password/', authapp.change_password, name='change_password'),
]

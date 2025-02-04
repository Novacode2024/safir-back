from . import auth_view
from django.urls import path, re_path

urlpatterns = [
    path('login/', auth_view.logIn, name='login'),
    path('logout/', auth_view.logOut, name='logout'),
]
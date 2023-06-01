from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_run, name='login'),
    path('register',views.register_run, name='register'),
    path('index',views.index_run, name='index'),
]
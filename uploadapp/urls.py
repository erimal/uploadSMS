from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('sendtest/', views.sendtest, name='sendtest'),

    path('login/', auth_views.LoginView.as_view(template_name='uploadapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='uploadapp/logout.html'), name='logout'),
]


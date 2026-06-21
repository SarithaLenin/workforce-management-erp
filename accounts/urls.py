"""
URL configuration for manpower_erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path('login/' ,login_view,name='login'),
   path('logout/' ,logout_view,name='logout'),
   path('users/', user_list, name='user_list'),
   path('users/add/', user_create, name='user_create'),
   path('users/<int:pk>/edit/',user_edit, name='user_edit'),
   path('users/<int:pk>/toggle-active/', user_toggle_active, name='user_toggle_active'),
   path('profile/', profile, name='profile'),
   path('change-password/', change_password, name='change_password'),
   path('profile/edit/', edit_profile, name='edit_profile'),
   path('settings/',settings_page, name='settings'),
   path('users/<int:pk>/reset-password/', admin_reset_password, name='admin_reset_password'),
  

]

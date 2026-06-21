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

    path('clients/',client_list,name='client_list'),
    path('clients/add/', client_create, name='client_create'),
    path('clients/<int:pk>/', client_detail, name='client_detail'),
    path('clients/<int:pk>/edit/', client_update, name='client_update'),
    path('clients/<int:pk>/delete/', client_delete, name='client_delete'),

    path('projects/', project_site_list, name='project_site_list'),
    path('projects/add/', project_site_create, name='project_site_create'),
    path('projects/<int:pk>/', project_site_detail, name='project_site_detail'),
    path('projects/<int:pk>/edit/', project_site_update, name='project_site_update'),
    path('projects/<int:pk>/delete/', project_site_delete, name='project_site_delete'),

    path('assignments/', assignment_list, name='assignment_list'),
    path('assignments/add/', assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/edit/', assignment_update, name='assignment_update'),
    path('assignments/<int:pk>/delete/', assignment_delete, name='assignment_delete'),

]

    




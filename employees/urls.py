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
    path('employees/', employee_list, name='employee_list'),
    path('employees/add/', employee_create, name='employee_create'),
    path('employees/<int:pk>/', employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', employee_delete, name='employee_delete'),
    path('employees/<int:pk>/documents/add/',employee_document_create,name='employee_document_create'),
    path('documents/<int:pk>/edit/', employee_document_update, name='employee_document_update'),
    path('documents/<int:pk>/delete/',employee_document_delete,name='employee_document_delete'),
    path('documents/<int:pk>/files/add/',employee_document_file_add,name='employee_document_file_add'),
]

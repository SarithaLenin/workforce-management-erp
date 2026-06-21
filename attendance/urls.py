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

    path('attendance/',attendance_entry,name='attendance_entry'),
    path('attendance/list/',attendance_list, name='attendance_list'),
    path('attendance/<int:pk>/edit/',attendance_update,name='attendance_update'),
    path('attendance/<int:pk>/delete/',attendance_delete,name='attendance_delete'),
    path('attendance/export/',export_attendance_excel, name='export_attendance_excel'),
    path('attendance/bulk-edit/',attendance_bulk_edit, name='attendance_bulk_edit'),
    
]






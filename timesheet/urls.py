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
   path('timesheet/' ,timesheet_generate,name='timesheet_generate'),
   path('timesheet/list/',timesheet_list,name='timesheet_list'),
   path('timesheet/<int:pk>/',timesheet_detail,name='timesheet_detail'),
   path('export-excel/<int:pk>/',timesheet_export_excel,name='timesheet_export_excel'),
   path('timesheet/<int:pk>/approve/', timesheet_approve,name='timesheet_approve'),
   path('timesheet/<int:pk>/reopen/', timesheet_reopen,name='timesheet_reopen'),
   path('timesheet/<int:pk>/delete/',timesheet_delete, name='timesheet_delete'),
   path("timesheet/<int:pk>/print/",timesheet_print,name="timesheet_print",),

]

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
from . import views


urlpatterns = [

    path('payroll/generate/', views.generate_payroll, name='generate_payroll'),

    path('payroll/', views.payroll_list, name='payroll_list'),
    path(
    "payroll/<int:pk>/",
    views.payroll_detail,
    name="payroll_detail",
    ),
    path(
        "payroll/<int:pk>/deductions/add/",
        views.payroll_deduction_add,
        name="payroll_deduction_add",
    ),
    path(
        "payroll/deductions/<int:pk>/delete/",
        views.payroll_deduction_delete,
        name="payroll_deduction_delete",
    ),


    path(
        "payroll/<int:pk>/edit/",
        views.payroll_edit,
        name="payroll_edit",
    ),

    path(
        "payroll/deductions/<int:pk>/edit/",
        views.payroll_deduction_edit,
        name="payroll_deduction_edit",
    ),


    path(
        "payroll/<int:pk>/recalculate/",
        views.payroll_recalculate,
        name="payroll_recalculate",
    ),
    path(
        "payroll/<int:pk>/approve/",
        views.payroll_approve,
        name="payroll_approve",
    ),
    path(
        "payroll/<int:pk>/mark-paid/",
        views.payroll_mark_paid,
        name="payroll_mark_paid",
    ),
    path(
        "payroll/<int:pk>/delete/",
        views.payroll_delete,
        name="payroll_delete",
    ),


    path(
        "payroll/<int:pk>/reopen/",
        views.payroll_reopen,
        name="payroll_reopen",
    ),

    path(
        "payroll/<int:pk>/salary-slip/",
        views.salary_slip,
        name="salary_slip",
    ),

    path(
        "payroll/payments/process/",
        views.payroll_payment_process,
        name="payroll_payment_process",
    ),


    path(
        "payroll/<int:pk>/record-payment/",
        views.payroll_record_payment,
        name="payroll_record_payment",
    ),

]
   




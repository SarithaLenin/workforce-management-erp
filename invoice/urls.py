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
from django.urls import path
from . import views

urlpatterns = [
    path('invoices/', views.invoice_list, name='invoice_list'),

    path(
        'generate-invoice/<int:timesheet_id>/',
        views.generate_invoice,
        name='generate_invoice'
    ),

    path(
        'billing-rates/',
        views.billing_rate_list,
        name='billing_rate_list'
    ),

    path(
        'billing-rates/add/',
        views.billing_rate_create,
        name='billing_rate_create'
    ),

    path(
        'billing-rates/<int:pk>/',
        views.billing_rate_detail,
        name='billing_rate_detail'
    ),

    path(
    'billing-rates/<int:pk>/edit/',
    views.billing_rate_edit,
    name='billing_rate_edit'
),

path(
    'billing-rates/<int:pk>/delete/',
    views.billing_rate_delete,
    name='billing_rate_delete'
),

path(
    'generate-invoice/<int:timesheet_id>/',
    views.generate_invoice,
    name='generate_invoice'
),

path(
    'invoices/<int:pk>/',
    views.invoice_detail,
    name='invoice_detail'
),

path(
    'invoices/<int:pk>/print/',
    views.invoice_print,
    name='invoice_print'
),


path(
    'invoices/<int:pk>/edit/',
    views.invoice_edit,
    name='invoice_edit'
),

path(
    'invoices/<int:pk>/export-excel/',
    views.invoice_export_excel,
    name='invoice_export_excel'
),


path(
    'invoices/<int:pk>/delete/',
    views.invoice_delete,
    name='invoice_delete'
),

path(
    'invoices/<int:pk>/approve/',
    views.invoice_approve,
    name='invoice_approve'
),

path(
    'invoices/<int:pk>/mark-paid/',
    views.invoice_mark_paid,
    name='invoice_mark_paid'
),

# path(
#     'invoices/<int:pk>/pdf/',
#     views.invoice_pdf,
#     name='invoice_pdf'
# ),


path(
    'reports/outstanding-invoices/',
    views.outstanding_invoice_report,
    name='outstanding_invoice_report'
),


path(
    'reports/payment-collection/',
    views.payment_collection_report,
    name='payment_collection_report'
),

path(
    "invoices/<int:pk>/reopen/",
    views.invoice_reopen,
    name="invoice_reopen",
),


    
]

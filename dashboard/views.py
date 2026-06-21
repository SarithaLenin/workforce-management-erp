from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from companies.models import Company
from employees.models import *
from clients.models import *
from invoice.models import *
from timesheet.models import *
from invoice.models import *
from accounts.decorators import role_required

# Create your views here.

@login_required
def dashboard(request):

    total_companies = Company.objects.count()
    total_employees = Employee.objects.count()
    total_clients = Client.objects.count()
    total_projects = ProjectSite.objects.count()

    draft_invoices = Invoice.objects.filter(status='DRAFT').count()
    paid_invoices = Invoice.objects.filter(status='PAID').count()

    outstanding_amount = 0
    for invoice in Invoice.objects.filter(status='APPROVED'):
        outstanding_amount += sum(item.net_amount for item in invoice.items.all())

    collected_amount = 0
    for invoice in Invoice.objects.filter(status='PAID'):
        collected_amount += sum(item.net_amount for item in invoice.items.all())

    today = timezone.now().date()
    next_30_days = today + timedelta(days=30)

    passport_expiring = EmployeeDocument.objects.filter(
        document_type='PASSPORT',
        expiry_date__gte=today,
        expiry_date__lte=next_30_days
    ).count()

    visa_expiring = EmployeeDocument.objects.filter(
        document_type='VISA',
        expiry_date__gte=today,
        expiry_date__lte=next_30_days
    ).count()

    emirates_id_expiring = EmployeeDocument.objects.filter(
        document_type='EMIRATES_ID',
        expiry_date__gte=today,
        expiry_date__lte=next_30_days
    ).count()

    labour_card_expiring = EmployeeDocument.objects.filter(
        document_type='LABOUR_CARD',
        expiry_date__gte=today,
        expiry_date__lte=next_30_days
    ).count()

    recent_employees = Employee.objects.order_by('-id')[:2]

    recent_timesheets = MonthlyTimesheet.objects.order_by('-id')[:2]

    recent_invoices = Invoice.objects.order_by('-id')[:2]


    context = {
        'total_companies': total_companies,
        'total_employees': total_employees,
        'passport_expiring': passport_expiring,
        'visa_expiring': visa_expiring,
        'emirates_id_expiring': emirates_id_expiring,
        'labour_card_expiring': labour_card_expiring,
        'recent_employees': recent_employees,
        'total_clients': total_clients,
        'total_projects': total_projects,
        'draft_invoices': draft_invoices,
        'paid_invoices': paid_invoices,
        'outstanding_amount': outstanding_amount,
        'collected_amount': collected_amount,
        'recent_timesheets': recent_timesheets,
        'recent_invoices':  recent_invoices,
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
@role_required(["admin", "hr", "accountant"])
def document_alert_list(request, document_type):

    today = timezone.now().date()
    next_30_days = today + timedelta(days=30)

    documents = EmployeeDocument.objects.select_related(
        'employee',
        'employee__company',
        'employee__designation'
    ).filter(
        document_type=document_type,
        expiry_date__gte=today,
        expiry_date__lte=next_30_days
    ).order_by('expiry_date')

    context = {
        'documents': documents,
        'document_type': document_type,
    }

    return render(request,'dashboard/document_alert_list.html',context)

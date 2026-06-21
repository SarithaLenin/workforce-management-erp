from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from .models import *
from .forms import *
from django.utils import timezone
from datetime import timedelta
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required




# Create your views here.

@login_required
@role_required(["admin", "hr", "accountant"])
def employee_list(request):

    search = request.GET.get('search', '')
    company_id = request.GET.get('company', '')

    employees = Employee.objects.select_related(
        'company',
        'designation'
    ).prefetch_related(
        'documents'
    ).all().order_by('-id')

    if company_id:
        employees = employees.filter(company_id=company_id)

    if search:
        employees = employees.filter(
            Q(employee_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(nationality__icontains=search) |
            Q(passport_number__icontains=search) |
            Q(emirates_id_number__icontains=search) |
            Q(documents__document_number__icontains=search) |
            Q(company__name__icontains=search) |
            Q(designation__name__icontains=search)
        ).distinct()

    for emp in employees:
        passport_doc = emp.documents.filter(
            document_type='PASSPORT'
        ).first()

        emirates_doc = emp.documents.filter(
            document_type='EMIRATES_ID'
        ).first()

        emp.passport_doc_number = (
            passport_doc.document_number
            if passport_doc and passport_doc.document_number
            else "-"
        )

        emp.emirates_doc_number = (
            emirates_doc.document_number
            if emirates_doc and emirates_doc.document_number
            else "-"
        )

    companies = Company.objects.filter(
        is_active=True
    ).order_by('name')

    context = {
        'employees': employees,
        'companies': companies,
        'search': search,
        'company_id': company_id,
    }

    return render(
        request,
        'employees/employee_list.html',
        context
    )


@login_required
@role_required(["admin", "hr", "accountant"])
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    documents = employee.documents.prefetch_related('files').all()

    context = {
        'employee': employee,
        'documents': documents,
    }

    return render(request, 'employees/employee_detail.html', context)

@login_required
@role_required(["admin", "hr"])
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
@role_required(["admin", "hr"])
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
@role_required(["admin", "hr"])
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


@login_required
@role_required(["admin", "hr"])
def employee_document_create(request, pk):

    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST)

        files = request.FILES.getlist('files')

        if form.is_valid():
            document = form.save(commit=False)
            document.employee = employee
            document.save()

            for uploaded_file in files:
                EmployeeDocumentFile.objects.create(
                    document=document,
                    file=uploaded_file
                )

            return redirect('employee_detail', pk=employee.pk)

    else:
        form = EmployeeDocumentForm()

    return render(
        request,
        'employees/employee_document_form.html',
        {
            'form': form,
            'employee': employee
        }
    )

@login_required
@role_required(["admin", "hr"])
def employee_document_update(request, pk):

    document = get_object_or_404(EmployeeDocument, pk=pk)
    employee = document.employee

    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, instance=document)

        if form.is_valid():
            form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeDocumentForm(instance=document)

    return render(request, 'employees/employee_document_form.html', {
        'form': form,
        'employee': employee,
        'document': document,
    })



@login_required
@role_required(["admin", "hr"])
def employee_document_delete(request, pk):

    document = get_object_or_404(EmployeeDocument, pk=pk)
    employee = document.employee

    if request.method == 'POST':
        document.delete()
        return redirect('employee_detail', pk=employee.pk)

    return render(request, 'employees/employee_document_confirm_delete.html', {
        'document': document,
        'employee': employee,
    })



@login_required
@role_required(["admin", "hr"])
def employee_document_file_add(request, pk):

    document = get_object_or_404(EmployeeDocument, pk=pk)
    employee = document.employee

    if request.method == 'POST':

        files = request.FILES.getlist('files')

        for uploaded_file in files:
            EmployeeDocumentFile.objects.create(
                document=document,
                file=uploaded_file
            )

        return redirect('employee_detail', pk=employee.pk)

    return render(
        request,
        'employees/employee_document_file_form.html',
        {
            'document': document,
            'employee': employee
        }
    )


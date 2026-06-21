from django.shortcuts import render, get_object_or_404, redirect
from . models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

# Create your views here.

@login_required
@role_required(["admin", "hr", "accountant"])
def client_list(request):
    search = request.GET.get('search', '')

    clients = Client.objects.all().order_by('name')

    if search:
        clients = clients.filter(
            Q(name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(trn_number__icontains=search)
        )

    return render(request, 'clients/client_list.html', {
        'clients': clients,
        'search': search
    })



@login_required
@role_required(["admin", "hr", "accountant"])
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    projects = client.projects.all().order_by('-id')

    return render(request, 'clients/client_detail.html', {
        'client': client,
        'projects': projects
    })



@login_required
@role_required(["admin", "hr"])
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()

    return render(request, 'clients/client_form.html', {
        'form': form
    })



@login_required
@role_required(["admin", "hr"])
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/client_form.html', {
        'form': form
    })

@login_required
@role_required(["admin"])
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.delete()
        return redirect('client_list')

    return render(request, 'clients/client_confirm_delete.html', {
        'client': client
    })



@login_required
@role_required(["admin", "hr", "accountant"])
def project_site_list(request):
    search = request.GET.get('search', '')

    projects = ProjectSite.objects.select_related('client').all().order_by('-id')

    if search:
        projects = projects.filter(
            Q(name__icontains=search) |
            Q(client__name__icontains=search) |
            Q(location__icontains=search) |
            Q(lpo_number__icontains=search) |
            Q(project_code__icontains=search)
        )

    return render(request, 'clients/project_site_list.html', {
        'projects': projects,
        'search': search
    })



@login_required
@role_required(["admin", "hr", "accountant"])
def project_site_detail(request, pk):
    project = get_object_or_404(ProjectSite, pk=pk)

    return render(request, 'clients/project_site_detail.html', {
        'project': project
    })



@login_required
@role_required(["admin", "hr"])
def project_site_create(request):
    if request.method == 'POST':
        form = ProjectSiteForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect('project_site_list')
    else:
        form = ProjectSiteForm()

    return render(request, 'clients/project_site_form.html', {
        'form': form
    })



@login_required
@role_required(["admin", "hr"])
def project_site_update(request, pk):
    project = get_object_or_404(ProjectSite, pk=pk)

    if request.method == 'POST':
        form = ProjectSiteForm(request.POST,request.FILES, instance=project)

        if form.is_valid():
            form.save()
            return redirect('project_site_detail', pk=project.pk)
    else:
        form = ProjectSiteForm(instance=project)

    return render(request, 'clients/project_site_form.html', {
        'form': form
    })


@login_required
@role_required(["admin"])
def project_site_delete(request, pk):
    project = get_object_or_404(ProjectSite, pk=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('project_site_list')

    return render(request, 'clients/project_site_confirm_delete.html', {
        'project': project
    })



@login_required
@role_required(["admin", "hr", "accountant"])
def assignment_list(request):
    search = request.GET.get('search', '')

    assignments = EmployeeAssignment.objects.select_related(
        'employee',
        'designation',
        'project_site',
        'project_site__client'
    ).all().order_by('-id')

    if search:
        assignments = assignments.filter(
            Q(employee__employee_id__icontains=search) |
            Q(employee__first_name__icontains=search) |
            Q(employee__last_name__icontains=search) |
            Q(designation__name__icontains=search) |
            Q(project_site__name__icontains=search) |
            Q(project_site__client__name__icontains=search)
        )

    return render(request, 'clients/assignment_list.html', {
        'assignments': assignments,
        'search': search
    })



@login_required
@role_required(["admin", "hr"])
def assignment_create(request):
    if request.method == 'POST':
        form = EmployeeAssignmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = EmployeeAssignmentForm()

    return render(request, 'clients/assignment_form.html', {
        'form': form
    })



@login_required
@role_required(["admin", "hr"])
def assignment_update(request, pk):
    assignment = get_object_or_404(EmployeeAssignment, pk=pk)

    if request.method == 'POST':
        form = EmployeeAssignmentForm(request.POST, instance=assignment)

        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = EmployeeAssignmentForm(instance=assignment)

    return render(request, 'clients/assignment_form.html', {
        'form': form
    })


@login_required
@role_required(["admin", "hr"])
def assignment_delete(request, pk):
    assignment = get_object_or_404(EmployeeAssignment, pk=pk)

    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list')

    return render(request, 'clients/assignment_confirm_delete.html', {
        'assignment': assignment
    })
                  


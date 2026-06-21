from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from .forms import CompanyForm
from .models import Company


@login_required
@role_required(["admin", "accountant", "hr"])
def company_list(request):
    search = request.GET.get("search", "").strip()

    companies = Company.objects.order_by("name")

    if search:
        companies = companies.filter(
            Q(name__icontains=search)
            | Q(code__icontains=search)
        )

    paginator = Paginator(companies, 10)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "companies/company_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        },
    )


@login_required
@role_required(["admin"])
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Company created successfully.",
            )
            return redirect("company_list")
    else:
        form = CompanyForm()

    return render(
        request,
        "companies/company_form.html",
        {"form": form},
    )


@login_required
@role_required(["admin"])
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":
        form = CompanyForm(
            request.POST,
            request.FILES,
            instance=company,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Company updated successfully.",
            )
            return redirect("company_list")
    else:
        form = CompanyForm(instance=company)

    # This must remain outside the else block so an
    # invalid submitted form can be displayed again.
    return render(
        request,
        "companies/company_form.html",
        {
            "form": form,
            "company": company,
        },
    )


@login_required
@role_required(["admin"])
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":
        try:
            company.delete()

            messages.success(
                request,
                "Company deleted successfully.",
            )
        except ProtectedError:
            messages.error(
                request,
                (
                    "This company has related business records "
                    "and cannot be deleted. Mark it inactive instead."
                ),
            )

        return redirect("company_list")

    return render(
        request,
        "companies/company_confirm_delete.html",
        {"company": company},
    )

    

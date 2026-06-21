from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from employees.models import Employee
from companies.models import Company
from django.db.models import Sum
from timesheet.models import MonthlyTimesheet, MonthlyTimesheetRow
import calendar
from django.db import transaction
from django.utils import timezone
from .models import Payroll, PayrollDeduction
from .services import recalculate_payroll
from django.views.decorators.http import require_POST
from .forms import (PayrollDeductionForm,PayrollEditForm,PayrollPaymentBatchForm,PayrollPaymentFilterForm,PayrollReopenForm,)
from .models import (Payroll,PayrollDeduction,PayrollPaymentBatch,PayrollPaymentItem,)
from accounts.decorators import role_required
# Create your views here.


@role_required(["admin", "accountant"])
@login_required
@transaction.atomic
def generate_payroll(request):
    companies = Company.objects.filter(
        is_active=True
    ).order_by("name")

    context = {
        "companies": companies,
        "months": list(
            enumerate(calendar.month_name[1:], start=1)
        ),
        "current_year": timezone.now().year,
        "selected_month": request.POST.get("month", ""),
        "selected_year": request.POST.get("year", ""),
        "selected_company": request.POST.get("company", ""),
    }

    if request.method != "POST":
        return render(
            request,
            "payroll/generate_payroll.html",
            context,
        )

    try:
        month = int(request.POST["month"])
        year = int(request.POST["year"])
    except (KeyError, TypeError, ValueError):
        messages.error(
            request,
            "Select a valid month and year.",
        )
        return render(
            request,
            "payroll/generate_payroll.html",
            context,
        )

    if month not in range(1, 13):
        messages.error(request, "Invalid payroll month.")
        return render(
            request,
            "payroll/generate_payroll.html",
            context,
        )

    company = Company.objects.filter(
        pk=request.POST.get("company"),
        is_active=True,
    ).first()

    if not company:
        messages.error(request, "Select a valid company.")
        return render(
            request,
            "payroll/generate_payroll.html",
            context,
        )

    # Generate payroll only for employees appearing
    # in approved timesheets for this period.
    employee_ids = MonthlyTimesheetRow.objects.filter(
        employee__isnull=False,
        employee__company=company,
        timesheet__month=month,
        timesheet__year=year,
        timesheet__status="APPROVED",
    ).values_list(
        "employee_id",
        flat=True,
    ).distinct()

    employees = Employee.objects.filter(
        id__in=employee_ids,
        company=company,
        is_active=True,
    ).select_related("company")

    created_count = 0
    updated_count = 0
    skipped_count = 0

    for employee in employees:
        payroll, created = Payroll.objects.get_or_create(
            employee=employee,
            month=month,
            year=year,
            defaults={
                "company": company,
                "generated_by": request.user,
            },
        )

        if not created and payroll.status != "DRAFT":
            skipped_count += 1
            continue

        # Save monthly salary snapshots.
        payroll.company = company
        payroll.salary_type = employee.salary_type
        payroll.basic_salary = (
            employee.basic_salary or Decimal("0.00")
        )
        payroll.food_allowance = (
            employee.food_allowance or Decimal("0.00")
        )
        payroll.hourly_rate = (
            employee.hourly_rate or Decimal("0.00")
        )

        if created:
            payroll.generated_by = request.user

        payroll.save()
        recalculate_payroll(payroll)

        if created:
            created_count += 1
        else:
            updated_count += 1

    if not created_count and not updated_count and not skipped_count:
        messages.warning(
            request,
            "No employees were found in an approved timesheet.",
        )
    else:
        messages.success(
            request,
            (
                f"Draft payroll generated: "
                f"{created_count} created, "
                f"{updated_count} recalculated, "
                f"{skipped_count} finalized records skipped."
            ),
        )

    return redirect("payroll_list")



@login_required
@role_required(["admin", "accountant", "hr"])
def payroll_list(request):
    month = request.GET.get("month", "")
    year = request.GET.get("year", "")
    company_id = request.GET.get("company", "")
    status = request.GET.get("status", "")
    search = request.GET.get("search", "").strip()

    # Create the queryset before applying filters.
    payrolls = Payroll.objects.select_related(
        "employee",
        "company",
    ).order_by(
        "-year",
        "-month",
        "employee__employee_id",
    )

    if month:
        payrolls = payrolls.filter(month=month)

    if year:
        payrolls = payrolls.filter(year=year)

    if company_id:
        payrolls = payrolls.filter(company_id=company_id)

    if status:
        payrolls = payrolls.filter(status=status)

    if search:
        payrolls = payrolls.filter(
            Q(employee__first_name__icontains=search)
            | Q(employee__last_name__icontains=search)
            | Q(employee__employee_id__icontains=search)
        )

    total_employees = payrolls.count()

    total_payroll = (
        payrolls.aggregate(total=Sum("net_salary"))["total"]
        or Decimal("0.00")
    )

    context = {
        "payrolls": payrolls,
        "companies": Company.objects.filter(
            is_active=True
        ).order_by("name"),
        "months": list(
            enumerate(calendar.month_name[1:], start=1)
        ),
        "month": month,
        "year": year,
        "company_id": company_id,
        "status": status,
        "search": search,
        "total_employees": total_employees,
        "total_payroll": total_payroll,
        "hourly_count": payrolls.filter(
            salary_type="HOURLY"
        ).count(),
        "basic_count": payrolls.filter(
            salary_type="BASIC"
        ).count(),
    }

    return render(
        request,
        "payroll/payroll_list.html",
        context,
    )



@login_required
@role_required(["admin", "accountant", "hr"])
def payroll_detail(request, pk):
    payroll = get_object_or_404(
        Payroll.objects.select_related(
            "employee",
            "company",
            "generated_by",
        ).prefetch_related("deductions"),
        pk=pk,
    )

    deduction_form = PayrollDeductionForm()

    payment_item = (
        PayrollPaymentItem.objects.select_related(
            "batch",
            "batch__processed_by",
        )
        .filter(
            payroll=payroll,
            batch__status="COMPLETED",
        )
        .order_by("-id")
        .first()
    )

    return render(
        request,
        "payroll/payroll_detail.html",
        {
            "payroll": payroll,
            "deduction_form": deduction_form,
            "payment_item": payment_item,
        },
    )


@login_required
@role_required(["admin", "accountant"])
@require_POST
def payroll_deduction_add(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)

    if payroll.status != "DRAFT":
        messages.error(
            request,
            "Deductions can only be changed in draft payroll.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    form = PayrollDeductionForm(request.POST)

    if form.is_valid():
        deduction = form.save(commit=False)
        deduction.payroll = payroll
        deduction.save()

        recalculate_payroll(payroll)

        messages.success(
            request,
            "Deduction added and salary recalculated.",
        )
    else:
        error_message = " ".join(
            error
            for errors in form.errors.values()
            for error in errors
        )
        messages.error(request, error_message)

    return redirect("payroll_detail", pk=payroll.pk)


@login_required
@role_required(["admin", "accountant"])
@require_POST
def payroll_deduction_delete(request, pk):
    deduction = get_object_or_404(
        PayrollDeduction.objects.select_related("payroll"),
        pk=pk,
    )
    payroll = deduction.payroll

    if payroll.status != "DRAFT":
        messages.error(
            request,
            "Deductions cannot be deleted after approval.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    deduction.delete()
    recalculate_payroll(payroll)

    messages.success(
        request,
        "Deduction deleted and salary recalculated.",
    )

    return redirect("payroll_detail", pk=payroll.pk)




@login_required
@role_required(["admin", "accountant"])
def payroll_edit(request, pk):
    payroll = get_object_or_404(
        Payroll.objects.select_related(
            "employee",
            "company",
        ),
        pk=pk,
    )

    if payroll.status != "DRAFT":
        messages.error(
            request,
            "Only draft payroll can be edited.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    if payroll.salary_type != "BASIC":
        messages.error(
            request,
            "This edit screen is for basic-salary payroll.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    if request.method == "POST":
        form = PayrollEditForm(
            request.POST,
            instance=payroll,
        )

        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.manually_updated_by = request.user
            payroll.manually_updated_at = timezone.now()
            payroll.save()

            recalculate_payroll(payroll)

            messages.success(
                request,
                "Payroll changes saved and salary recalculated.",
            )
            return redirect(
                "payroll_detail",
                pk=payroll.pk,
            )
    else:
        form = PayrollEditForm(
            instance=payroll,
            initial={
                "manual_adjustment_reason": "",
            },
        )

    return render(
        request,
        "payroll/payroll_edit.html",
        {
            "payroll": payroll,
            "form": form,
        },
    )



@login_required
@role_required(["admin", "accountant"])
def payroll_deduction_edit(request, pk):
    deduction = get_object_or_404(
        PayrollDeduction.objects.select_related(
            "payroll",
            "payroll__employee",
        ),
        pk=pk,
    )
    payroll = deduction.payroll

    if payroll.status != "DRAFT":
        messages.error(
            request,
            "Deductions cannot be edited after approval.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    if request.method == "POST":
        form = PayrollDeductionForm(
            request.POST,
            instance=deduction,
        )

        if form.is_valid():
            form.save()
            recalculate_payroll(payroll)

            messages.success(
                request,
                "Deduction updated and salary recalculated.",
            )
            return redirect(
                "payroll_detail",
                pk=payroll.pk,
            )
    else:
        form = PayrollDeductionForm(instance=deduction)

    return render(
        request,
        "payroll/payroll_deduction_edit.html",
        {
            "payroll": payroll,
            "deduction": deduction,
            "form": form,
        },
    )



@login_required

@role_required(["admin", "accountant"])
@require_POST
def payroll_recalculate(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)

    if payroll.status != "DRAFT":
        messages.error(
            request,
            "Only draft payroll can be recalculated.",
        )
    else:
        recalculate_payroll(payroll)
        messages.success(
            request,
            "Payroll recalculated successfully.",
        )

    return redirect("payroll_detail", pk=payroll.pk)



@login_required
@role_required(["admin", "accountant"])
@require_POST
@transaction.atomic
def payroll_approve(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)

    if payroll.status != "DRAFT":
        messages.error(
            request,
            "Only draft payroll can be approved.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    recalculate_payroll(payroll)

    payroll.status = "APPROVED"
    payroll.approved_by = request.user
    payroll.approved_at = timezone.now()
    payroll.save()

    messages.success(
        request,
        "Payroll approved and locked.",
    )

    return redirect("payroll_detail", pk=payroll.pk)




@login_required
@role_required(["admin", "accountant"])
@require_POST
def payroll_mark_paid(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)

    if payroll.status != "APPROVED":
        messages.error(
            request,
            "Only approved payroll can be marked as paid.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    payroll.status = "PAID"
    payroll.paid_by = request.user
    payroll.paid_at = timezone.now()
    payroll.save()

    messages.success(
        request,
        "Payroll marked as paid.",
    )

    return redirect("payroll_detail", pk=payroll.pk)


@login_required
@role_required(["admin"])
@require_POST
def payroll_delete(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)

    if payroll.status != "DRAFT":
        messages.error(
            request,
            "Only draft payroll can be deleted.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    payroll.delete()

    messages.success(
        request,
        "Draft payroll deleted.",
    )

    return redirect("payroll_list")



@login_required
@role_required(["admin"])
def payroll_reopen(request, pk):
    payroll = get_object_or_404(
        Payroll.objects.select_related(
            "employee",
            "company",
        ),
        pk=pk,
    )

    if payroll.status != "APPROVED":
        messages.error(
            request,
            "Only approved, unpaid payroll can be reopened.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    if request.method == "POST":
        form = PayrollReopenForm(request.POST)

        if form.is_valid():
            payroll.status = "DRAFT"
            payroll.reopened_by = request.user
            payroll.reopened_at = timezone.now()
            payroll.reopen_reason = form.cleaned_data["reason"]
            payroll.save()

            messages.success(
                request,
                "Payroll reopened. Changes can now be made.",
            )

            return redirect(
                "payroll_detail",
                pk=payroll.pk,
            )
    else:
        form = PayrollReopenForm()

    return render(
        request,
        "payroll/payroll_reopen.html",
        {
            "payroll": payroll,
            "form": form,
        },
    )



@login_required
@role_required(["admin", "accountant", "hr"])
def salary_slip(request, pk):
    payroll = get_object_or_404(
        Payroll.objects.select_related(
            "employee",
            "company",
            "approved_by",
            "paid_by",
        ).prefetch_related("deductions"),
        pk=pk,
    )

    if payroll.status == "DRAFT":
        messages.error(
            request,
            "Approve payroll before printing the salary slip.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    return render(
        request,
        "payroll/salary_slip.html",
        {"payroll": payroll},
    )

@role_required(["admin", "accountant"])
@login_required
def payroll_payment_process(request):
    filter_data = (
        request.POST
        if request.method == "POST"
        else request.GET
    )

    filter_form = PayrollPaymentFilterForm(
        filter_data or None
    )
    payment_form = PayrollPaymentBatchForm(
        request.POST or None
    )

    payrolls = Payroll.objects.none()
    company = None
    month = None
    year = None

    if filter_form.is_valid():
        company = filter_form.cleaned_data["company"]
        month = int(filter_form.cleaned_data["month"])
        year = filter_form.cleaned_data["year"]

        payrolls = Payroll.objects.filter(
            company=company,
            month=month,
            year=year,
            status="APPROVED",
        ).select_related(
            "employee",
            "company",
        ).order_by(
            "employee__employee_id"
        )

        if request.method == "POST":
            selected_ids = {
                value
                for value in request.POST.getlist(
                    "payroll_ids"
                )
                if value.isdigit()
            }

            if not selected_ids:
                messages.error(
                    request,
                    "Select at least one employee.",
                )

            elif payment_form.is_valid():
                with transaction.atomic():
                    selected_payrolls = list(
                        Payroll.objects.select_for_update()
                        .filter(
                            id__in=selected_ids,
                            company=company,
                            month=month,
                            year=year,
                            status="APPROVED",
                        )
                        .select_related("employee")
                    )

                    if len(selected_payrolls) != len(selected_ids):
                        messages.error(
                            request,
                            (
                                "Some selected payrolls are no "
                                "longer approved or available."
                            ),
                        )
                    else:
                        total_amount = sum(
                            (
                                payroll.net_salary
                                for payroll in selected_payrolls
                            ),
                            Decimal("0.00"),
                        )

                        batch = payment_form.save(commit=False)
                        batch.company = company
                        batch.month = month
                        batch.year = year
                        batch.employee_count = len(
                            selected_payrolls
                        )
                        batch.total_amount = total_amount
                        batch.processed_by = request.user
                        batch.save()

                        PayrollPaymentItem.objects.bulk_create(
                            [
                                PayrollPaymentItem(
                                    batch=batch,
                                    payroll=payroll,
                                    paid_amount=payroll.net_salary,
                                )
                                for payroll in selected_payrolls
                            ]
                        )

                        paid_time = timezone.now()

                        Payroll.objects.filter(
                            id__in=[
                                payroll.id
                                for payroll in selected_payrolls
                            ]
                        ).update(
                            status="PAID",
                            paid_by=request.user,
                            paid_at=paid_time,
                        )

                        messages.success(
                            request,
                            (
                                f"{len(selected_payrolls)} "
                                f"employees marked as paid. "
                                f"Total: AED {total_amount:.2f}"
                            ),
                        )

                        return redirect("payroll_list")

    preselected_payroll_id = (
        request.POST.get("individual_payroll_id", "")
        if request.method == "POST"
        else request.GET.get("payroll", "")
    )

    context = {
        "filter_form": filter_form,
        "payment_form": payment_form,
        "payrolls": payrolls,
        "company": company,
        "selected_month": month,
        "selected_year": year,
        "selected_total": payrolls.aggregate(
            total=Sum("net_salary")
        )["total"] or Decimal("0.00"),

        "preselected_payroll_id": preselected_payroll_id,
    }

    return render(
        request,
        "payroll/payroll_payment_process.html",
        context,
    )


@role_required(["admin", "accountant"])
@login_required
def payroll_record_payment(request, pk):
    payroll = get_object_or_404(
        Payroll.objects.select_related(
            "employee",
            "company",
        ),
        pk=pk,
    )

    if payroll.status != "APPROVED":
        messages.error(
            request,
            "Only approved payroll can be paid.",
        )
        return redirect("payroll_detail", pk=payroll.pk)

    if request.method == "POST":
        form = PayrollPaymentBatchForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                locked_payroll = (
                    Payroll.objects.select_for_update()
                    .get(pk=payroll.pk)
                )

                if locked_payroll.status != "APPROVED":
                    messages.error(
                        request,
                        "This payroll is no longer available.",
                    )
                    return redirect(
                        "payroll_detail",
                        pk=payroll.pk,
                    )

                batch = form.save(commit=False)
                batch.company = payroll.company
                batch.month = payroll.month
                batch.year = payroll.year
                batch.employee_count = 1
                batch.total_amount = payroll.net_salary
                batch.processed_by = request.user
                batch.save()

                PayrollPaymentItem.objects.create(
                    batch=batch,
                    payroll=locked_payroll,
                    paid_amount=locked_payroll.net_salary,
                )

                locked_payroll.status = "PAID"
                locked_payroll.paid_by = request.user
                locked_payroll.paid_at = timezone.now()
                locked_payroll.save()

            messages.success(
                request,
                "Employee salary marked as paid.",
            )

            return redirect(
                "payroll_detail",
                pk=payroll.pk,
            )
    else:
        form = PayrollPaymentBatchForm(
            initial={"payment_method": "CASH"}
        )

    return render(
        request,
        "payroll/payroll_record_payment.html",
        {
            "payroll": payroll,
            "form": form,
        },
    )
